from django.urls import path
from .views import ItineraryListView

urlpatterns = [
    path("trips/<str:trip_title>/",ItineraryListView.as_view(),name="itinerary-list")
]