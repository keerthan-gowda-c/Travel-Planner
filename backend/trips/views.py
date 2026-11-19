
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from django.db import transaction
from django.db.models import F

from .models import Trip, TripStop
from .serializers import (
    TripSerializer,
    TripStopSerializer,
    RecommendationRequestSerializer,
)
from .recommendation import recommend_destination

from subscriptions.models import Subscription
from trips.access import has_premium_access, has_trip_access



class TripListCreateView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

    def perform_create(self, serializer):
        with transaction.atomic():
            subscription, _ = Subscription.objects.get_or_create(
                user=self.request.user,
                defaults={"plan": "free", "status": "free"}
            )

            # Premium users can create trips without using credits.
            if has_premium_access(self.request.user):
                serializer.save(
                    user=self.request.user,
                    requires_payment=False
                )
                return

            # First three trips are free.
            if subscription.free_trips_created < 3:
                serializer.save(
                    user=self.request.user,
                    requires_payment=False
                )

                Subscription.objects.filter(
                    pk=subscription.pk
                ).update(
                    free_trips_created=F("free_trips_created") + 1
                )
                return

            # Use one extra-trip credit if available.
            credit_used = Subscription.objects.filter(
                pk=subscription.pk,
                extra_trip_credits__gt=0
            ).update(
                extra_trip_credits=F("extra_trip_credits") - 1
            )

            if credit_used:
                serializer.save(
                    user=self.request.user,
                    requires_payment=False
                )
                return

            # No free trips, Premium or extra credits.
            # Individual ₹49 payment is required.
            serializer.save(
                user=self.request.user,
                requires_payment=True
            )


class DashboardTripListView(generics.ListAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trip.objects.filter(
            user=self.request.user
        ).order_by("-created_at")


class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "title"
    lookup_url_kwarg = "trip_title"

    def get_queryset(self):
        # Basic trip details remain visible for the payment workflow.
        return Trip.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class TripStopListCreateView(generics.ListCreateAPIView):
    serializer_class = TripStopSerializer
    permission_classes = [IsAuthenticated]

    def get_trip(self):
        try:
            trip = Trip.objects.get(
                title__iexact=self.kwargs["trip_title"],
                user=self.request.user,
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied(
                "Payment is required to access this trip's stops."
            )

        return trip

    def get_queryset(self):
        trip = self.get_trip()

        return TripStop.objects.filter(
            trip=trip
        ).order_by("order")

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
        try:
            trip = Trip.objects.get(
                title__iexact=self.kwargs["trip_title"],
                user=self.request.user,
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied(
                "Payment is required to access this trip's stops."
            )

        return TripStop.objects.filter(trip=trip)


class TripActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_title):
        try:
            trip = Trip.objects.get(
                title__iexact=trip_title,
                user=request.user
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if trip.status == "active":
            return Response(
                {"detail": "This trip is already active."},
                status=http_status.HTTP_200_OK
            )

        if trip.status in ["completed", "cancelled"]:
            raise ValidationError({
                "detail": "Completed or cancelled trips cannot be activated."
            })

        if not has_trip_access(request.user, trip):
            raise PermissionDenied(
                "Payment is required before activating this trip."
            )

        if not has_premium_access(request.user):
            another_active_trip = Trip.objects.filter(
                user=request.user,
                status="active"
            ).exclude(pk=trip.pk).exists()

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

        if not has_trip_access(request.user, trip):
            raise PermissionDenied(
                "Payment is required before completing this trip."
            )

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

        if not has_premium_access(request.user):
            return Response({
                "detail": (
                    "Destination recommendations are available only "
                    "for Premium users. Please upgrade your plan."
                )
            }, status=http_status.HTTP_403_FORBIDDEN)

        try:
            recommendations = recommend_destination(
                origin=data["origin"],
                start_date=data["start_date"],
                end_date=data["end_date"],
                budget=data["budget"],
                travel_mode=data["travel_mode"],
            )

        except ValueError as error:
            raise ValidationError({"origin": str(error)})

        if not recommendations:
            return Response({
                "detail": "No destinations found within your budget.",
                "recommendations": [],
            }, status=http_status.HTTP_200_OK)

        return Response({
            "origin": data["origin"],
            "recommendations": recommendations,
        }, status=http_status.HTTP_200_OK)
