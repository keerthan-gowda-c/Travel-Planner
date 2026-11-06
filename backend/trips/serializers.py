from rest_framework import serializers
from .models import Trip, TripStop
from subscriptions.models import Subscription
from decimal import Decimal

class TripSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    destination = serializers.CharField(max_length=100)
    class Meta:
        model = Trip
        fields = ["id","title","origin","destination","image_url","start_date","end_date","budget","status","requires_payment","created_at"]
        read_only_fields = ["id","status","requires_payment","created_at"]

    def validate(self, data):
        start_date = data.get("start_date",getattr(self.instance, "start_date", None))
        end_date = data.get("end_date",getattr(self.instance, "end_date", None))
        budget = data.get("budget",getattr(self.instance, "budget", None))

        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"end_date": "End date must be on or after the start date."})

        if budget is not None and budget <= 0:
            raise serializers.ValidationError({"budget": "Budget must be greater than zero"})

        request = self.context.get("request")

        if request and start_date and end_date:
            subscription, _ = Subscription.objects.get_or_create(user=request.user,defaults={"plan": "free", "status": "free"})
            is_premium = (subscription.plan == "premium" and subscription.status == "active")
            trip_days = (end_date - start_date).days + 1

            if not is_premium and trip_days > 3:
                raise serializers.ValidationError({
                    "end_date": (
                        "Free users can plan trips lasting a maximum "
                        "of 3 calendar days. Upgrade to Premium for longer trips."
                    )
                })

        return data



class TripStopSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TripStop
        fields = [
            "id",
            "trip",
            "name",
            "arrival_date",
            "order",
            "notes",
        ]
        read_only_fields = ["id", "trip"]

    def validate(self, data):
        stop = self.instance
        trip = stop.trip if stop else self.context.get("trip")

        arrival_date = data.get(
            "arrival_date",
            getattr(stop, "arrival_date", None) if stop else None,
        )

        if trip and arrival_date:
            if arrival_date < trip.start_date or arrival_date > trip.end_date:
                raise serializers.ValidationError({
                    "arrival_date": "Stop date must be within the trip dates."
                })

        return data


class RecommendationRequestSerializer(serializers.Serializer):
    TRANSPORT_CHOICES = [
        ("train", "Train"),
        ("bus", "Bus"),
        ("car", "Car"),
        ("flight", "Flight"),
    ]

    origin = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    budget = serializers.DecimalField(max_digits=12,decimal_places=2,min_value=Decimal("0.01"))
    travel_mode = serializers.ChoiceField(choices=TRANSPORT_CHOICES)

    def validate(self, data):
        if data["end_date"] < data["start_date"]:
            raise serializers.ValidationError({"end_date":"End date must be on or after the start date."})

        return data
