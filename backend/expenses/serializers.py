
from rest_framework import serializers
from .models import Expenses
from trips.models import Trip


class StringPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return str(value.pk)


class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    trips = StringPrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = Expenses
        fields = ["id","trips","category","description","amount","expense_date"]
        read_only_fields = ["id"]

    def validate_trips(self,trip):
        request = self.context.get("request")

        if request and trip.user != request.user:
            raise serializers.ValidationError("You can only add expenses to your own trips.")

        return trip

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return amount

    def validate(self, data):
        expense = self.instance

        trip = data.get("trips",expense.trips if expense else None)
        expense_date = data.get("expense_date",expense.expense_date if expense else None)

        if trip and expense_date:
            if not trip.start_date <= expense_date <= trip.end_date:
                raise serializers.ValidationError({"expense_date": ("Expense date must be within the trip dates.")})

        return data
 