from django.urls import path
from .views import ItineraryListCreateView, ItineraryDetailView

urlpatterns = [
    path("<str:trip_title>/",ItineraryListCreateView.as_view(),name="itinerary-list-create"),
    path("<str:trip_title>/<str:itinerary_id>/",ItineraryDetailView.as_view(),name="itinerary-detail"),

]