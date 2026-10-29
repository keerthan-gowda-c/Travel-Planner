from rest_framework import serializers
from .models import Subscription

class SubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Subscription
        fields = ["id","plan","billing_period","status","current_period_start","current_period_end"]
        read_only_fields = fields