from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Subscription(models.Model):
    PLAN_CHOICES = [("free","Free"),("premium","Premium")]
    BILLING_CHOICES = [("weekly", "Weekly"),("monthly","Monthly")]

    STATUS_CHOICES = [
        ("free", "Free"),
        ("created", "Created"),
        ("authenticated", "Authenticated"),
        ("active", "Active"),
        ("pending", "Pending"),
        ("halted", "Halted"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired"),
        ("failed", "Failed"),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="subscriptions")
    plan = models.CharField(max_length=20,choices=PLAN_CHOICES,default="free")
    billing_period = models.CharField(max_length=20,choices=BILLING_CHOICES,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="free")
    free_trips_created = models.PositiveIntegerField(default=0)
    razorpay_subscription_id = models.CharField(max_length=100,blank=True,null=True,unique=True)
    current_period_start = models.DateTimeField(blank=True,null=True)
    current_period_end = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.status})"