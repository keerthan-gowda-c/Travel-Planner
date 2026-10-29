from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Trip(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget =models. DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="scheduled")
    requires_payment = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination or 'Not selected'}"

class TripStop(models.Model):
    trip=models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="stops")
    name=models.CharField(max_length=150)
    arrival_date=models.DateField(blank=True,null=True)
    order = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.name}"

