from django.db import models
from django.contrib.auth.models import User
from trips.models import Trip
# Create your models here.

class TripPayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_TYPE_CHOICES = [
        ("extra_trip", "Extra Trip"),
        ("extra_trip_bundle", "Extra Trip Bundle"),
        ("trip_extension", "Trip Extension"),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="trip_payments")
    trip = models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True,blank=True,related_name="payments")
    payment_type = models.CharField(max_length=30,choices=PAYMENT_TYPE_CHOICES,default="extra_trip")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,default="pending")
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True,unique=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        trip_title = self.trip.title if self.trip else "No linked trip"
        return f"{self.user.username} - {self.payment_type} - {trip_title} - {self.status}"
