from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound,ValidationError
from .models import Trip, TripStop
from .serializers import TripSerializer,TripStopSerializer, RecommendationRequestSerializer
from subscriptions.models import Subscription
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from payments.models import TripPayment
from .recommendation import recommend_destination

# Create your views here.

class TripListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(user=self.request.user).order_by("-created_at")
    
    def perform_create(self, serializer):
        subscription, _ = Subscription.objects.get_or_create(user=self.request.user,defaults={"plan": "free", "status": "free"})
        is_premium = (subscription.plan == "premium"and subscription.status == "active")
        
        if is_premium:
            serializer.save(user=self.request.user,requires_payment=False)
            return

        if subscription.free_trips_created < 3:
            serializer.save(user=self.request.user,requires_payment=False)

            subscription.free_trips_created += 1
            subscription.save(update_fields=["free_trips_created"])

        else:
            serializer.save(user=self.request.user,requires_payment=True)

class DashboardTripListView(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        subscription, _ = Subscription.objects.get_or_create(
            user=self.request.user,
            defaults={"plan": "free", "status": "free"}
        )

        is_premium = (
            subscription.plan == "premium"
            and subscription.status == "active"
        )

        trips = Trip.objects.filter(user=self.request.user)

        if is_premium:
            return trips.order_by("-created_at")

        return trips.filter(
            requires_payment=False
        ).order_by("-created_at")[:3]

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "title"
    lookup_url_kwarg = "trip_title"

    def get_queryset(self):
        return Trip.objects.filter(
            user=self.request.user
        )

    def perform_destroy(self, instance):
        instance.delete()

class TripStopListCreateView(generics.ListCreateAPIView):
    serializer_class = TripStopSerializer
    permission_classes = [IsAuthenticated]

    def get_trip(self):
        try:
            return Trip.objects.get(
                title=self.kwargs["trip_title"],
                user=self.request.user,
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

    def get_queryset(self):
        trip = self.get_trip()
        return TripStop.objects.filter(trip=trip).order_by("order")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["trip"] = self.get_trip()
        return context

    def perform_create(self, serializer):
        serializer.save(trip=self.get_trip())


class TripStopDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripStopSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "stop_id"

    def get_queryset(self):
        return TripStop.objects.filter(
            trip__user=self.request.user,
            trip__title=self.kwargs["trip_title"],
        )


class TripActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_title):
        try:
            trip = Trip.objects.get(title__iexact=trip_title,user=request.user)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if trip.status == "active":
            return Response({"detail": "This trip is already active."},status=http_status.HTTP_200_OK)

        if trip.status in ["completed", "cancelled"]:
            raise ValidationError({"detail": "Completed or cancelled trips cannot be activated."})

        subscription, _ = Subscription.objects.get_or_create(user=request.user,defaults={"plan": "free", "status": "free"})
        is_premium = (subscription.plan == "premium" and subscription.status == "active")

        if trip.requires_payment and not is_premium:
            payment_exists = TripPayment.objects.filter(user=request.user,trip=trip,status="paid").exists()

            if not payment_exists:
                raise ValidationError({"detail":"Payment is required before activating this trip."})
            
        if not is_premium:
            another_active_trip = Trip.objects.filter(user=request.user,status="active",).exclude(pk=trip.pk).exists()

            if another_active_trip:
                raise ValidationError({
                    "detail": (
                        "You already have an active trip. "
                        "Complete or cancel it before activating another."
                    )
                })

        trip.status = "active"
        trip.save(update_fields=["status"])

        return Response({
            "detail": "Trip activated successfully.",
            "title": trip.title,
            "status": trip.status,
        })

class TripCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_title):
        try:
            trip = Trip.objects.get(
                title__iexact=trip_title,
                user=request.user,
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if trip.status != "active":
            raise ValidationError({
                "detail": "Only an active trip can be completed."
            })

        trip.status = "completed"
        trip.save(update_fields=["status"])

        return Response({
            "detail": "Trip completed successfully.",
            "title": trip.title,
            "status": trip.status,
        })

class DestinationRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RecommendationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        subscription, _ = Subscription.objects.get_or_create(user=request.user,defaults={"plan":"free", "status":"free"})

        is_premium = (subscription.plan == "premium" and subscription.status == "active")

        if not is_premium:
            return Response({
                "detail":("Destination recommendation are available only for Premium user. Please upgrade your plan" )
            }, status=http_status.HTTP_403_FORBIDDEN)

        try:
            recommendations = recommend_destination(origin=data["origin"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                budget=data["budget"],
                travel_mode=data["travel_mode"],)

        except ValueError as error:
            raise ValidationError({"origin": str(error)})

        if not recommendations:
            return Response(
                {"detail": "No destinations found within your budget.","recommendations": [],},
                status=http_status.HTTP_200_OK,
            )

        return Response(
            {"origin": data["origin"],"recommendations": recommendations,},
            status=http_status.HTTP_200_OK,
        )