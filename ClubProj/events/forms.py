from django import forms
from .models import Venue, Event


class DateTimePicker(forms.DateTimeInput):
    input_type='datetime-local'


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ("name", "address", "pin_code", "phone_no", "email_address")

        labels = {
            'name': '',
            'address': '',
            'pin_code': '',
            'phone_no': '',
            'email_address': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
            'pin_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Pin code'}),
            'phone_no': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("name", "event_date", "venue", "manager", "description", "attendees")

        labels = {
            'name': '',
            'event_date': '',
            'venue': '',
            'manager': '',
            'description': '',
            'attendees': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Event Name'}),
            #'event_date': DateTimePicker(attrs={'class':'form-control'}),
            'event_date':  forms.TextInput(attrs={'class':'form-control', 'placeholder': 'YYYY-MM-DD HH:MM:SS'}),
            'venue': forms.Select(attrs={'class':'form-control'}),
            'manager': forms.Select(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Any description'}),
            'attendees': forms.SelectMultiple(attrs={'class':'form-control'}),
        }


