from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget =models. DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination or 'Not selected'}"