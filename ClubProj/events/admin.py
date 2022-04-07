from re import search
from warnings import filters
from django.contrib import admin

# Register your models here.
from .models import Venue, MyClubUser, Event

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'pin_code', 'phone_no')
    ordering = ("name",)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager')
    list_display = ('name', 'event_date','venue')
    list_filter = ('event_date','venue') 
    ordering = ('-event_date', )