from rest_framework import serializers
from .models import Trip

class TripSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Trip
        fields = ["id","title","origin","destination","start_date","end_date","budget","created_at"]
        read_only_fields = ["id","destination","created_at"]

    def validate(self, data):
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError("End date must be on or after the start date.")

        if data["budget"] <= 0:
            raise serializers.ValidationError("Budget must be greater than zero")

        return data
