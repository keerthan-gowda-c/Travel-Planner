from django.urls import path
from .views import (TripListCreateView,TripDetailView,
                    TripStopListCreateView,TripStopDetailView,DashboardTripListView,
                    TripActivateView,TripCompleteView,DestinationRecommendationView)

urlpatterns = [
    path("dashboard/", DashboardTripListView.as_view(), name="dashboard-trips"),
    path("",TripListCreateView.as_view(),name="trip-list-create"),
    path("recommend/",DestinationRecommendationView.as_view(),name="destination-recommendation"),
    path("<str:trip_title>/activate/",TripActivateView.as_view(),name="trip-activate"),
    path("<str:trip_title>/stops/",TripStopListCreateView.as_view(),name="trip-stop-list-create"),
    path("<str:trip_title>/stops/<str:stop_id>/",TripStopDetailView.as_view(),name="trip-stop-detail"),
    path("<str:trip_title>/complete/",TripCompleteView.as_view(),name="trip-complete"),
    path("<str:trip_title>/",TripDetailView.as_view(),name="trip-detail"),

]