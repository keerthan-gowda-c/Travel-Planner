from django.shortcuts import render
from .serializers import SubscriptionSerializer

import razorpay

from django.conf import settings
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from trips.access import has_premium_access
# Create your views here.


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        subscription, _ = Subscription.objects.get_or_create(user=request.user,defaults={"plan":"free","status":"free"})

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data)

class CreatePremiumSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        billing_period = request.data.get("billing_period")

        plans = {
            "weekly": {"plan_id": settings.RAZORPAY_WEEKLY_PLAN_ID,"total_count": 520},
            "monthly": {"plan_id": settings.RAZORPAY_MONTHLY_PLAN_ID,"total_count": 120}
        }

        if billing_period not in plans:
            raise ValidationError({"billing_period":"Choose Weekly or monthly"})

        existing_subscription = Subscription.objects.filter(
            user=request.user
        ).first()

        if existing_subscription and existing_subscription.status in [
            "created",
            "authenticated",
            "pending",
            "halted",
        ]:
            raise ValidationError(
                "You already have a subscription being processed. "
                "Please complete or resolve it before creating another."
            )

        if has_premium_access(request.user):
            raise ValidationError("You already have an active Premium subscription")

        plan = plans[billing_period]

        if not plan["plan_id"]:
            raise ValidationError("Razorpay plan Id is not configured.")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

        try:
            razorpay_subscription = client.subscription.create({
                "plan_id": plan["plan_id"],
                "total_count": plan["total_count"],
                "customer_notify": 1,
                "notes": {
                    "user_id": str(request.user.pk),
                    "billing_period": billing_period
                }
            })

        except Exception:
            raise ValidationError(
                "Unable to create subscription. Please try again."
            )

        subscription, _ = Subscription.objects.get_or_create(
            user=request.user
        )

        subscription.plan = "premium"
        subscription.billing_period = billing_period
        subscription.status = "created"
        subscription.cancel_at_period_end = False
        subscription.razorpay_subscription_id = (
            razorpay_subscription["id"]
        )

        subscription.current_period_start = None
        subscription.current_period_end = None

        subscription.save()

        return Response({
            "subscription_id": razorpay_subscription["id"],
            "key_id": settings.RAZORPAY_KEY_ID,
            "plan": "premium",
            "billing_period": billing_period,
            "status": "created"
        }, status=http_status.HTTP_201_CREATED)


class VerifyPremiumSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("razorpay_payment_id")
        subscription_id = request.data.get("razorpay_subscription_id")
        signature = request.data.get("razorpay_signature")

        if not all([payment_id, subscription_id, signature]):
            raise ValidationError({
                "detail": "Payment ID, subscription ID and signature are required."
            })

        try:
            subscription = Subscription.objects.get(
                user=request.user,
                razorpay_subscription_id=subscription_id
            )
        except Subscription.DoesNotExist:
            raise ValidationError(
                "Subscription not found for this user."
            )

        if subscription.status not in ["created", "authenticated"]:
            raise ValidationError(
                "This subscription cannot be verified in its current state."
            )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        try:
            client.utility.verify_subscription_signature({
                "razorpay_payment_id": payment_id,
                "razorpay_subscription_id": subscription_id,
                "razorpay_signature": signature
            })

        except razorpay.errors.SignatureVerificationError:
            raise ValidationError(
                "Subscription signature verification failed."
            )

        subscription.status = "authenticated"
        subscription.save(update_fields=["status", "updated_at"])

        return Response({
            "detail": "Subscription signature verified successfully.",
            "subscription_status": subscription.status,
            "message": (
                "Premium access will be enabled after Razorpay "
                "confirms subscription activation."
            )
        }, status=http_status.HTTP_200_OK)


class CancelPremiumSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription = Subscription.objects.filter(
            user=request.user
        ).first()

        if not subscription or not subscription.razorpay_subscription_id:
            raise ValidationError(
                "No Razorpay subscription found."
            )

        if subscription.cancel_at_period_end:
            raise ValidationError(
                "Your subscription is already scheduled for cancellation."
            )

        if subscription.status not in ["active", "created", "authenticated"]:
            raise ValidationError(
                "This subscription cannot be cancelled in its current state."
            )

        # Active subscriptions are cancelled at the end
        # of the current billing cycle.
        cancel_at_cycle_end = subscription.status == "active"

        if cancel_at_cycle_end and not has_premium_access(request.user):
            raise ValidationError(
                "Your Premium subscription is not currently active."
            )

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        try:
            client.subscription.cancel(
                subscription.razorpay_subscription_id,
                {
                    "cancel_at_cycle_end": cancel_at_cycle_end
                }
            )

        except Exception:
            raise ValidationError(
                "Unable to cancel your subscription. Please try again."
            )

        if cancel_at_cycle_end:
            # Keep Premium access until the paid period ends.
            subscription.cancel_at_period_end = True
        else:
            # No active billing cycle: cancel immediately.
            subscription.plan = "free"
            subscription.status = "cancelled"
            subscription.billing_period = ""
            subscription.cancel_at_period_end = False

        subscription.save()

        return Response({
            "detail": (
                "Your Premium subscription will be cancelled "
                "at the end of the current billing period."
                if cancel_at_cycle_end
                else "Your Premium subscription has been cancelled."
            ),
            "status": subscription.status,
            "cancel_at_period_end": subscription.cancel_at_period_end,
            "current_period_end": subscription.current_period_end,
        }, status=http_status.HTTP_200_OK)

import hmac
import hashlib

class RazorpayWebhookView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET

        if not webhook_secret:
            return Response(
                {"detail": "Webhook secret is not configured."},
                status=http_status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        signature = request.headers.get("X-Razorpay-Signature")

        if not signature:
            return Response(
                {"detail": "Missing webhook signature."},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        expected_signature = hmac.new(
            webhook_secret.encode("utf-8"),
            request.body,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return Response(
                {"detail": "Invalid webhook signature."},
                status=http_status.HTTP_400_BAD_REQUEST
            )

        # Event processing will be added in the next step.
        return Response(
            {"detail": "Webhook received."},
            status=http_status.HTTP_200_OK
        )