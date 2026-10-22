from django.shortcuts import render
from django.db import transaction
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Trip
from .serializers import TripSerializer
from .recommendation import recommend_destination
from itineraries.models import Itinerary
from itineraries.planner import generate_itinerary

# Create your views here.


class TripCreateView(generics.CreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]
        budget = serializer.validated_data["budget"]
        origin = serializer.validated_data["origin"]

        recommendation = recommend_destination(origin,start_date,end_date,budget)

        if recommendation is None:
            raise ValidationError("No destination fits your budget for these dates")

        trip = serializer.save(user=self.request.user, destination=recommendation["name"])
        itinerary_items = generate_itinerary(trip)
        Itinerary.objects.bulk_create([Itinerary(**item) for item in itinerary_items])
