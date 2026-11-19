from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from trips.models import Trip
from .models import Itinerary
from .serializers import ItinerarySerializer
from trips.access import has_trip_access
# Create your views here.

class ItineraryListCreateView(generics.ListCreateAPIView):
    serializer_class = ItinerarySerializer
    permission_classes =[IsAuthenticated]

    def get_trip(self):
        trip_title = self.kwargs["trip_title"]

        try:
            trip = Trip.objects.get(title__iexact=trip_title,user=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied("Payment is required to access this trip's itinerary")

        return trip

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
        try:
            trip = Trip.objects.get(title__iexact=self.kwargs["trip_title"],user=self.request.user)
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if not has_trip_access(self.request.user, trip):
            raise PermissionDenied("Payment is required to access this trip's itinerary.")

        return Itinerary.objects.filter(trip=trip) 

    