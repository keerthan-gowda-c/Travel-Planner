from django.db import models
from trips.models import Trip

# Create your models here.
class Itinerary(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE,related_name="iteneraries")
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField()
    estimated_cost = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"