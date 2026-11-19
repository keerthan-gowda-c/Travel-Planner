from django.urls import path
from .views import MySubscriptionView, CreatePremiumSubscriptionView, VerifyPremiumSubscriptionView, RazorpayWebhookView, CancelPremiumSubscriptionView

urlpatterns = [
    path("me/",MySubscriptionView.as_view(),name="my-subscription"),
    path("create",CreatePremiumSubscriptionView.as_view(),name="create-premium-subscription"),
    path("verify/",VerifyPremiumSubscriptionView.as_view(),name="verify-premium-subscription"),
    path("cancel/",CancelPremiumSubscriptionView.as_view(),name="cancel-premium-subscription"),
    path("webhook/",RazorpayWebhookView.as_view(),name="razorpay-webhook"),

]