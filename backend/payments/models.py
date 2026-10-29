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
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="trip_payments")
    trip = models.ForeignKey(Trip,on_delete=models.SET_NULL,null=True,blank=True,related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES,default="pending")
    rayzorpay_order_id = models.CharField(max_length=100,blank=True,null=True,unique=True)
    rayzorpay_payment_id = models.CharField(max_length=100,blank=True,null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        trip_title = self.trip.title if self.trip else "Deleted trip"
        return f"{self.user.username} - {trip_title} - {self.status}"
