
from django.utils import timezone

from subscriptions.models import Subscription
from payments.models import TripPayment


def has_premium_access(user):
    subscription = Subscription.objects.filter(user=user).first()

    if not subscription:
        return False

    if subscription.plan != "premium":
        return False

    if subscription.status not in ["active", "cancelled"]:
        return False

    now = timezone.now()

    # Premium access requires a valid paid-through date.
    if not subscription.current_period_end:
        return False

    # Expired subscriptions automatically revert to Free.
    if subscription.current_period_end <= now:
        subscription.plan = "free"
        subscription.status = "expired"
        subscription.billing_period = ""
        subscription.cancel_at_period_end = False
        subscription.save(update_fields=[
            "plan",
            "status",
            "billing_period",
            "cancel_at_period_end",
            "updated_at",
        ])
        return False

    return True


def has_trip_access(user, trip):
    if trip.user_id != user.id:
        return False

    # Premium users can access their trips.
    if has_premium_access(user):
        return True

    # Free trips and bundle-credit-funded trips.
    if not trip.requires_payment:
        return True

    # Only a successful individual Extra Trip payment
    # can unlock a payment-required trip.
    return TripPayment.objects.filter(
        user=user,
        trip=trip,
        payment_type="extra_trip",
        status="paid",
    ).exists()
