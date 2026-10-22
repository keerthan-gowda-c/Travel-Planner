from django.db import models
from trips.models import Trip
# Create your models here.


class Expenses(models.Model):
    CATEGORY_CHOICES =  [
        ("transport", "Transport"),
        ("accommodation", "Accommodation"),
        ("food", "Food"),
        ("activities", "Activities"),
        ("other", "Other"),
    ]

    trips = models.ForeignKey(Trip,on_delete=models.CASCADE,related_name="expenses")
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    expense_date = models.DateField()

    def __str__(self):
        return f"{self.category}: {self.amount}"