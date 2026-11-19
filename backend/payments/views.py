from django.shortcuts import render
import razorpay
from django.db.models import F
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from rest_framework import status as http_status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import TripPayment
from trips.models import Trip
from subscriptions.models import Subscription
from trips.access import has_premium_access
from .pricing import EXTRA_TRIP_PRICE, CURRENCY, EXTRA_TRIP_BUNDLE_PRICE,EXTRA_TRIP_BUNDLE_QUANTITY
# Create your views here.


class TripPaymentOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, trip_title):
        try:
            trip = Trip.objects.get(title__iexact=trip_title,user=request.user)

        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        if has_premium_access(request.user):
            raise ValidationError(
                "Premium users don't need individual trip payments."
            )
        if not trip.requires_payment:
            raise ValidationError("This trip does not require an additional payment.")

        existing_payment = TripPayment.objects.filter(user=request.user,trip=trip,payment_type="extra_trip",status="paid").exists()
        
        if existing_payment:
            raise ValidationError("this trip has already been paid for.")

        pending_payment = TripPayment.objects.filter(
            trip=trip,
            user=request.user,
            status="pending"
        ).first()

        if pending_payment:
            return Response({
                "order_id": pending_payment.razorpay_order_id,
                "amount": int(pending_payment.amount * 100),
                "currency": CURRENCY,
                "key_id": settings.RAZORPAY_KEY_ID,
            }, status=http_status.HTTP_200_OK)
    
        amount_rupees = EXTRA_TRIP_PRICE
        amount_paise = amount_rupees * 100

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        order = client.order.create({
            "amount":amount_paise,
            "currency":CURRENCY,
            "receipt":f"trip_{trip.pk}"
        })

        TripPayment.objects.create(user=request.user,trip=trip,amount=amount_rupees,status="pending",razorpay_order_id=order["id"])

        return Response({
            "order_id":order["id"],
            "amount":amount_paise,
            "currency":CURRENCY,
            "key_id":settings.RAZORPAY_KEY_ID
        },status=http_status.HTTP_201_CREATED)


class TripPaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, trip_title):
        try:
            trip = Trip.objects.get(
                title__iexact=trip_title,
                user=request.user
            )
        except Trip.DoesNotExist:
            raise NotFound("Trip not found.")

        order_id = request.data.get("razorpay_order_id")
        payment_id = request.data.get("razorpay_payment_id")
        signature = request.data.get("razorpay_signature")

        if not all([order_id, payment_id, signature]):
            raise ValidationError({
                "detail": (
                    "Order ID, payment ID, and signature are required."
                )
            })

        try:
            payment_record = TripPayment.objects.get(
                user=request.user,
                trip=trip,
                payment_type="extra_trip",
                razorpay_order_id=order_id,
            )
        except TripPayment.DoesNotExist:
            raise NotFound("Payment order not found.")

        # Make verification retries safe.
        if payment_record.status == "paid":
            if payment_record.razorpay_payment_id == payment_id:
                return Response({
                    "detail": "Payment has already been verified.",
                    "trip_title": trip.title,
                    "payment_status": payment_record.status,
                }, status=http_status.HTTP_200_OK)

            raise ValidationError({
                "detail": "This order has already been paid."
            })

        if payment_record.status != "pending":
            raise ValidationError({
                "detail": "This payment order is no longer pending."
            })

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        # Verify the signature on the backend.
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
        except razorpay.errors.SignatureVerificationError:
            raise ValidationError({
                "detail": "Payment signature verification failed."
            })

        # Confirm the payment belongs to this order and is captured.
        try:
            razorpay_payment = client.payment.fetch(payment_id)
        except Exception:
            raise ValidationError({
                "detail": (
                    "Unable to confirm the payment with Razorpay. "
                    "Please try again."
                )
            })

        if razorpay_payment.get("order_id") != order_id:
            raise ValidationError({
                "detail": "Payment does not belong to this order."
            })

        if razorpay_payment.get("status") != "captured":
            raise ValidationError({
                "detail": (
                    "Payment has not been captured yet. "
                    "Please try again after confirmation."
                )
            })

        if razorpay_payment.get("amount") != int(
            payment_record.amount * 100
        ):
            raise ValidationError({
                "detail": "Payment amount does not match the order."
            })

        if razorpay_payment.get("currency") != CURRENCY:
            raise ValidationError({
                "detail": "Payment currency does not match the order."
            })

        payment_record.razorpay_payment_id = payment_id
        payment_record.status = "paid"
        payment_record.paid_at = timezone.now()

        payment_record.save(update_fields=[
            "razorpay_payment_id",
            "status",
            "paid_at",
        ])

        return Response({
            "detail": "Payment verified successfully.",
            "trip_title": trip.title,
            "payment_status": payment_record.status,
        }, status=http_status.HTTP_200_OK)



class ExtraTripBundleOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Reuse an existing pending bundle order if available.
        pending_payment = TripPayment.objects.filter(
            user=request.user,
            payment_type="extra_trip_bundle",
            status="pending",
        ).first()

        if pending_payment:
            return Response({
                "order_id": pending_payment.razorpay_order_id,
                "amount": int(pending_payment.amount * 100),
                "currency": CURRENCY,
                "key_id": settings.RAZORPAY_KEY_ID,
                "quantity": EXTRA_TRIP_BUNDLE_QUANTITY,
            }, status=http_status.HTTP_200_OK)

        amount_paise = EXTRA_TRIP_BUNDLE_PRICE * 100

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        order = client.order.create({
            "amount": amount_paise,
            "currency": CURRENCY,
            "receipt": f"bundle_{request.user.pk}_{int(timezone.now().timestamp())}",
        })

        TripPayment.objects.create(
            user=request.user,
            trip=None,
            payment_type="extra_trip_bundle",
            amount=EXTRA_TRIP_BUNDLE_PRICE,
            status="pending",
            razorpay_order_id=order["id"],
        )

        return Response({
            "order_id": order["id"],
            "amount": amount_paise,
            "currency": CURRENCY,
            "key_id": settings.RAZORPAY_KEY_ID,
            "quantity": EXTRA_TRIP_BUNDLE_QUANTITY,
        }, status=http_status.HTTP_201_CREATED)


class ExtraTripBundleVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("razorpay_order_id")
        payment_id = request.data.get("razorpay_payment_id")
        signature = request.data.get("razorpay_signature")

        if not all([order_id, payment_id, signature]):
            raise ValidationError({
                "detail": "Order ID, payment ID, and signature are required."
            })

        try:
            payment_record = TripPayment.objects.get(
                user=request.user,
                payment_type="extra_trip_bundle",
                razorpay_order_id=order_id,
            )
        except TripPayment.DoesNotExist:
            raise NotFound("Bundle payment order not found.")

        # Prevent duplicate credit allocation.
        if payment_record.status == "paid":
            if payment_record.razorpay_payment_id == payment_id:
                subscription = Subscription.objects.get(user=request.user)

                return Response({
                    "detail": "Bundle payment has already been verified.",
                    "payment_status": "paid",
                    "credits_added": EXTRA_TRIP_BUNDLE_QUANTITY,
                    "available_credits": subscription.extra_trip_credits,
                }, status=http_status.HTTP_200_OK)

            raise ValidationError({
                "detail": "This order has already been paid."
            })

        if payment_record.status != "pending":
            raise ValidationError({
                "detail": "This payment order is no longer pending."
            })

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )

        # Verify Razorpay signature.
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
        except razorpay.errors.SignatureVerificationError:
            raise ValidationError({
                "detail": "Payment signature verification failed."
            })

        # Fetch and verify the actual Razorpay payment.
        try:
            razorpay_payment = client.payment.fetch(payment_id)
        except Exception:
            raise ValidationError({
                "detail": "Unable to confirm payment with Razorpay. Please try again."
            })

        if razorpay_payment.get("order_id") != order_id:
            raise ValidationError({
                "detail": "Payment does not belong to this order."
            })

        if razorpay_payment.get("status") != "captured":
            raise ValidationError({
                "detail": "Payment has not been captured yet."
            })

        if razorpay_payment.get("amount") != int(
            payment_record.amount * 100
        ):
            raise ValidationError({
                "detail": "Payment amount does not match the order."
            })

        if razorpay_payment.get("currency") != CURRENCY:
            raise ValidationError({
                "detail": "Payment currency does not match the order."
            })

        # Mark payment as paid and allocate credits only once.
        with transaction.atomic():
            updated = TripPayment.objects.filter(
                pk=payment_record.pk,
                status="pending",
            ).update(
                razorpay_payment_id=payment_id,
                status="paid",
                paid_at=timezone.now(),
            )

            if updated == 1:
                Subscription.objects.get_or_create(user=request.user)

                Subscription.objects.filter(
                    user=request.user
                ).update(
                    extra_trip_credits=(
                        F("extra_trip_credits")
                        + EXTRA_TRIP_BUNDLE_QUANTITY
                    )
                )

            else:
                payment_record.refresh_from_db()

                if (
                    payment_record.status == "paid"
                    and payment_record.razorpay_payment_id == payment_id
                ):
                    subscription = Subscription.objects.get(
                        user=request.user
                    )

                    return Response({
                        "detail": "Bundle payment has already been verified.",
                        "payment_status": "paid",
                        "available_credits": subscription.extra_trip_credits,
                    }, status=http_status.HTTP_200_OK)

                raise ValidationError({
                    "detail": "This payment could not be processed. Please try again."
                })

        subscription = Subscription.objects.get(user=request.user)

        return Response({
            "detail": "Bundle payment verified successfully.",
            "payment_status": "paid",
            "credits_added": EXTRA_TRIP_BUNDLE_QUANTITY,
            "available_credits": subscription.extra_trip_credits,
        }, status=http_status.HTTP_200_OK)
