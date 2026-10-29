from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from .models import Expenses
from .serializers import ExpenseSerializer
from decimal import Decimal
from django.db.models import Sum
from trips.models import Trip
# Create your views here.


class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expenses.objects.filter(trips__user=self.request.user).order_by("-expense_date")

    def perform_create(self, serializer):
        trip = serializer.validated_data["trips"]

        if trip.user != self.request.user:
            raise PermissionDenied("You can only add expenses to your own trips.")

        serializer.save()


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "expense_id"

    def get_queryset(self):
        return Expenses.objects.filter(trips__user=self.request.user)

class ExpenseSummaryView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request, trip_title):
        try:
            trip = Trip.objects.get(title__iexact=trip_title,user=request.user)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        expenses = Expenses.objects.filter(trips=trip)

        total_spent = (expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00"))
        category_summary = (expenses.values("category").annotate(total=Sum("amount")).order_by("category"))

        return Response({
            "title":trip.title,
            "destination": trip.destination,
            "budget": trip.budget,
            "total_spent": total_spent,
            "remaining_budget": trip.budget - total_spent,
            "category_summary": list(category_summary),
        })