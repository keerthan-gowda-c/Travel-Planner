
from decimal import Decimal

from django.db.models import Sum
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from .models import Expense
from .serializers import ExpenseSerializer
from trips.models import Trip
from trips.access import has_trip_access


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_trips = [
            trip for trip in Trip.objects.filter(user=user)
            if has_trip_access(user, trip)
        ]

        return Expense.objects.filter(
            trip__in=accessible_trips
        ).order_by("-expense_date")

    def perform_create(self, serializer):
        trip = serializer.validated_data["trip"]

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied(
                "Payment is required before adding expenses to this trip."
            )

        serializer.save()


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "expense_id"

    def get_queryset(self):
        user = self.request.user

        accessible_trips = [
            trip for trip in Trip.objects.filter(user=user)
            if has_trip_access(user, trip)
        ]

        return Expense.objects.filter(
            trip__in=accessible_trips
        )

    def perform_update(self, serializer):
        trip = serializer.validated_data.get(
            "trip",
            serializer.instance.trip
        )

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied(
                "Payment is required before adding expenses to this trip."
            )

        serializer.save()


class ExpenseSummaryView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trip_title):
        try:
            trip = Trip.objects.get(
                title__iexact=trip_title,
                user=request.user
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if not has_trip_access(request.user, trip):
            raise PermissionDenied(
                "Payment is required before accessing this trip's expenses."
            )

        expenses = Expense.objects.filter(trip=trip)

        total_spent = (
            expenses.aggregate(total=Sum("amount"))["total"]
            or Decimal("0.00")
        )

        category_summary = (
            expenses.values("category")
            .annotate(total=Sum("amount"))
            .order_by("category")
        )

        return Response({
            "title": trip.title,
            "destination": trip.destination,
            "budget": trip.budget,
            "total_spent": total_spent,
            "remaining_budget": trip.budget - total_spent,
            "category_summary": list(category_summary),
        })
