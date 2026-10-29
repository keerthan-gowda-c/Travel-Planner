from django.urls import path
from .views import TripPaymentOrderView, TripPaymentVerifyView

urlpatterns = [
    path("trips/<str:trip_title>/order/",TripPaymentOrderView.as_view(),name="trip-payment-order"),
    path("trips/<str:trip_title>/verify/",TripPaymentVerifyView.as_view(),name="trip-payment-verify")

]
