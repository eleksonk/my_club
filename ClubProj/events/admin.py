from django.contrib import admin
from django.contrib.auth.models import Group


# Register your models here.
from .models import Venue, MyClubUser, Event

#admin.site.register(Venue)
admin.site.register(MyClubUser)
#admin.site.register(Event)

#remove groups
#admin.site.unregister(Group)

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'pin_code', 'phone_no')
    ordering = ("name",)
    search_fields = ('name', 'address')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_date', 'description', 'manager', 'approved')
    list_display = ('name', 'event_date','venue')
    list_filter = ('event_date','venue') 
    ordering = ('-event_date', )