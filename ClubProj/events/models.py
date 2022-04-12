from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import default

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    pin_code = models.CharField('Pin code', max_length=6)
    phone_no =  models.CharField('Contact no ', max_length=10, blank=True)
    email_address = models.EmailField('Email address',  blank=True)
    owner = models.IntegerField("Venue owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email_address = models.EmailField('User Email address')

    def __str__(self):
        return self.first_name + ' ' +self.last_name

class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField('Event date')
    venue = models.ForeignKey(Venue, max_length=120, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField("Approved", default=False)

    def __str__(self):
        return self.name
    
    @property
    def Days_left(self):
        today = date.today()
        days_left = self.event_date.date() - today
        if self.event_date.date()< today :
            days_left_stripped = "Already over"
        else:
            days_left_stripped = str(days_left).split(",", 1)[0] + " left"
            
        return days_left_stripped
