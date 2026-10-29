from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from trips.models import Trip
from .models import Itinerary
from .serializers import ItinerarySerializer
# Create your views here.

class ItineraryListCreateView(generics.ListCreateAPIView):
    serializer_class = ItinerarySerializer
    permission_classes =[IsAuthenticated]

    def get_trip(self):
        trip_title = self.kwargs["trip_title"]

        try:
            return Trip.objects.get(title__iexact=trip_title,user=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

    def get_queryset(self):
        trip = self.get_trip()

        return Itinerary.objects.filter(trip=trip).order_by("day_number")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["trip"] = self.get_trip()
        return context

    def perform_create(self, serializer):
        serializer.save(trip=self.get_trip())


class ItineraryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItinerarySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "itinerary_id"

    def get_queryset(self):
        return Itinerary.objects.filter(
            trip__title__iexact=self.kwargs["trip_title"],
            trip__user=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["trip"] = self.get_object().first().trip
        return context
    