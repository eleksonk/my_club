from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin

from django.http import HttpResponse
import csv

#for pdf
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

#for pagination
from django.core.paginator import Paginator


from django.contrib import messages
from django.contrib.auth.models import User

from django.db.models import Q
import calendar
from datetime import datetime

# Create your views here.
def home(request):
    year = datetime.now().year
    month=datetime.now().strftime('%B')
    month = month.capitalize()
    
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number
        ) 
    return render(request, 'events/home.html', {"event_list": event_list})

def all_events(request):
    events = Event.objects.all().order_by("-event_date")
    return render(request, 'events/events_list.html', {'events':events})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id  #logged in user-id         
            venue.save() 
            #form.save()
            submitted = True
    else:            
        form = VenueForm()

    return render(request, 'events/add_venue.html', {'form' : form, 'submitted':submitted})


def all_venues(request):
    venue_lists= Venue.objects.all().order_by("name")
    #setup pagination , 2 venues at a time to display 
    p = Paginator(venue_lists, 2)
    page = request.GET.get('page')
    venues_pg = p.get_page(page)
    
    return render(request, 'events/venues.html', {'venues_pg': venues_pg})

def show_venue(request, pk):
    venue= Venue.objects.get(pk=pk)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue':venue, 'venue_owner': venue_owner})

def search_venues(request):
    if request.method == "POST":
        searched=request.POST["searched"]
        #icontains case insensitive
        venues =Venue.objects.filter(name__icontains = searched)
        return render(request, 'events/search_venues.html', {'searched':searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html')
    
def update_venue(request, pk):
    venue=get_object_or_404(Venue, pk=pk)
    form = VenueForm(request.POST or None, request.FILES or None, instance = venue)   
    if request.method == "POST":          
        if form.is_valid():
            form.save()
            return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'form':form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                submitted = True
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user  #logged in user         
                event.save() 
                submitted = True        
    else:
        if request.user.is_superuser:            
            form = EventFormAdmin()
        else:
            form = EventForm()

    return render(request, 'events/add_event.html', {'form' : form, 'submitted':submitted})

def update_event(request, pk):
    event=get_object_or_404(Event, pk=pk)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance = event)
        
    else:
        form = EventForm(request.POST or None, instance = event)
        
    if request.method == "POST":        
        if form.is_valid():
            form.save()
            return redirect('list-events')
            
    return render(request, 'events/update_event.html', {'event': event, 'form':form})

def delete_event(request, pk):    
    event=get_object_or_404(Event, pk=pk)
    if request.user == event.manager:
        event.delete()
        messages.success(request, "Event deleted successfully!!!")        
    else:
        messages.success(request, "You are not authorized")
        
    return redirect('list-events')
    
       

def delete_venue(request, pk):
    if request.user.is_authenticated:    
        venue=get_object_or_404(Venue, pk=pk)
        venue.delete()
        return redirect('list-venues')
    else:
        return redirect('login')

#Generate Text file of Venues
def venue_text(request):
    response = HttpResponse(content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename = venues.txt'
    
    venues = Venue.objects.all()
    #create blank list
    lines = []
    
    for venue in venues:
        lines.append(f'{venue.name}\n')
        lines.append(f'{venue.address}\n')
        lines.append(f'{venue.pin_code}\n')
        lines.append(f'{venue.phone_no}\n')
        lines.append(f'{venue.email_address}\n')
        lines.append(f'\n')
    
    
    response.writelines(lines)
    return response

#Generate Text file of Venues
def venue_csv(request):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename = venues.csv'
    
    writer = csv.writer(response)
     
     #Add column headings to the csv file
    writer.writerow(["Venue Name", "Address", "Pin Code", "Phone No", "Email Address"])
          
    venues = Venue.objects.all()
        
    for venue in venues:
        writer.writerow([venue.name, venue.address,venue.pin_code,venue.phone_no,venue.email_address])
    
    return response

def venue_pdf(request):
    buff = io.BytesIO()
    canv = canvas.Canvas(buff, pagesize=A4, bottomup=0)
    
    textobj = canv.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont('Helvetica', 14)
    
    venues = Venue.objects.all()
    #create blank list
    lines = []
    
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.pin_code)
        lines.append(venue.phone_no)
        lines.append(venue.email_address)
        lines.append("============================")
        
    for line in lines:
        textobj.textLine(line)        
    
    canv.drawText(textobj)
    canv.showPage()
    canv.save()
    buff.seek(0)
    
    return FileResponse(buff, as_attachment=True, filename='venues.pdf')

def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, "events/my_events.html", {"events": events})
    else:
        messages.success(request, "You are not authorized")
        return redirect('home')
    
def search_events(request):
    if request.method == "POST":
        searched=request.POST["searched"]
        
        #multiple column search
        lookup = Q(name__icontains = searched) | Q(description__icontains = searched)
        #icontains case insensitive
        events =Event.objects.filter(lookup)
        return render(request, 'events/search_events.html', {'searched':searched, 'events': events})
    else:
        return render(request, 'events/search_events.html')
    
def admin_approval(request):
    #get venue lists
    venue_list = Venue.objects.all()
    
    #Get counts
    event_count = Event.objects.filter(approved=True).count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    events = Event.objects.all().order_by("-event_date")
    if request.user.is_superuser:
        if request.method=="POST":            
            id_list = request.POST.getlist("boxes")
            
            #uncheck all events 
            events.update(approved=False)
            
            #update the database
            for id in id_list:
                Event.objects.filter(pk=int(id)).update(approved=True)
            
            messages.success(request, "Events Approved !!!")
            return redirect("list-events")            
    else:
        messages.success(request, "You are not authorized to access this page")
        return redirect('home')
    
    return render(request, 'events/admin_approval.html', {"events": events, 
                                                          "event_count":event_count, 
                                                          "venue_count": venue_count,
                                                          "user_count": user_count,
                                                          "venue_list": venue_list})

def venue_events(request, venue_id):
    #get the venue
    venue = Venue.objects.get(pk=venue_id)
    
    #get all events associated with this venue
    events = Event.objects.filter(venue=venue)
    #events = venue.event_set.all()
    
    if events:
        return render(request, 'events/venue_events.html', {"events": events})
    else:
        messages.success(request, "There are no events at this venue for this time")
        return redirect('admin-approval')
    
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)    
    return render(request, 'events/show_event.html', {"event": event})

        
    

