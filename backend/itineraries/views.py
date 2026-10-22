from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Itinerary
from .serializers import ItinerarySerializer
# Create your views here.

class ItineraryListView(generics.ListAPIView):
    serializer_class = ItinerarySerializer
    permission_classes =[IsAuthenticated]

    def get_queryset(self):
        trip_title = self.kwargs["trip_title"]
        return Itinerary.objects.filter(trip__title__iexact=trip_title,trip__user=self.request.user).order_by("day_number")