from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class House(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    amenities = models.CharField(max_length=100)
    max_guests = models.IntegerField()
    city = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guests = models.IntegerField(default=1)
    guest_names = models.TextField(default='No guest names provided')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.guest_names} - {self.house}'
    
    def save(self, *args, **kwargs):
        # Check if the house is available for the selected dates
        bookings = Booking.objects.filter(house=self.house, start_date__lte=self.end_date, end_date__gte=self.start_date)
        if bookings.exists():
            raise ValidationError("This house is not available for the selected dates.")
        if self.guests > self.house.max_guests:
            raise ValidationError("The number of guests exceeds the maximum capacity of the house.")
        super().save(*args, **kwargs)
  

    
    
