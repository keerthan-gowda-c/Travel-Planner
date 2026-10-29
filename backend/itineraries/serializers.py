
from rest_framework import serializers
from .models import Itinerary


class ItinerarySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Itinerary
        fields = [
            "id",
            "trip",
            "day_number",
            "title",
            "description",
            "estimated_cost",
        ]
        read_only_fields = ["id", "trip"]

    def validate(self, data):
        itinerary = self.instance
        trip = (
            itinerary.trip
            if itinerary
            else self.context.get("trip")
        )

        day_number = data.get(
            "day_number",
            itinerary.day_number if itinerary else None,
        )
        estimated_cost = data.get(
            "estimated_cost",
            itinerary.estimated_cost if itinerary else 0,
        )

        if day_number is not None and trip:
            trip_days = (trip.end_date - trip.start_date).days + 1

            if day_number < 1 or day_number > trip_days:
                raise serializers.ValidationError({
                    "day_number": (
                        f"Day number must be between 1 and {trip_days} "
                        "for this trip."
                    )
                })

        if estimated_cost is not None and estimated_cost < 0:
            raise serializers.ValidationError({
                "estimated_cost": "Estimated cost cannot be negative."
            })

        return data
