
from rest_framework import serializers
from .models import Expenses
from trips.models import Trip


class StringPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        return str(value.pk)


class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    trips = StringPrimaryKeyRelatedField(
        queryset=Trip.objects.all()
    )

    class Meta:
        model = Expenses
        fields = [
            "id",
            "trips",
            "category",
            "description",
            "amount",
            "expense_date",
        ]
        read_only_fields = ["id"]
