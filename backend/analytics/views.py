from django.shortcuts import render
from decimal import Decimal

from django.db.models import Sum, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from trips.models import Trip
from expenses.models import Expense
from trips.access import has_premium_access
# Create your views here.

class AnalyticsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        today = timezone.localdate()
        user = request.user

        user_trips = Trip.objects.filter(user=user)

        if has_premium_access(user):
            trips = user_trips
        else:
            trips = user_trips.filter(
                Q(requires_payment=False)
                | Q(payments__user=user, payments__status="paid")
            ).distinct()

        trips = trips.annotate(total_spent=Sum("expenses__amount"))
        upcoming_trips = trips.filter(start_date__gt=today).count()
        ongoing_trips = trips.filter(start_date__lte=today,end_date__gte=today,).count()
        completed_trips = trips.filter(end_date__lt=today).count()
        expenses = Expense.objects.filter(trips__user=request.user)
        total_budget = (trips.aggregate(total=Sum("budget"))["total"] or Decimal("0.00"))
        total_spent = (expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00"))
        category_summary = (expenses.values("category").annotate(total=Sum("amount")).order_by("category"))
        trip_comparison = []

        for trip in trips:
            spent = trip.total_spent or Decimal("0.00")

            trip_comparison.append({
                "title": trip.title,
                "destination": trip.destination,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "budget": trip.budget,
                "total_spent": spent,
                "remaining_budget": trip.budget - spent,
            })

        return Response({
            "total_trips" : trips.count(),
            "upcoming_trips": upcoming_trips,
            "ongoing_trips": ongoing_trips,
            "completed_trips": completed_trips,
            "total_budget" : total_budget,
            "total_spent" : total_spent,
            "remaining_budget":total_budget-total_spent,
            "category_summary" : list(category_summary),
            "trip_comparison" : trip_comparison
        })
