from django.urls import path
from .views import TripPaymentOrderView, TripPaymentVerifyView, ExtraTripBundleOrderView, ExtraTripBundleVerifyView

urlpatterns = [
    path("<str:trip_title>/order/",TripPaymentOrderView.as_view(),name="trip-payment-order"),
    path("<str:trip_title>/verify/",TripPaymentVerifyView.as_view(),name="trip-payment-verify"),
    path("bundle/order/",ExtraTripBundleOrderView.as_view(),name="extra-trip-bundle-order"),
    path("bundle/verify/",ExtraTripBundleVerifyView.as_view(),name="extra-trip-bundle-verify"),
]
