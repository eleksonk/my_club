from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Venue
from .forms import VenueForm, EventForm

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




# Create your views here.
def home(request):
    return render(request, 'events/home.html', {})

def all_events(request):
    events = Event.objects.all().order_by("event_date")
    return render(request, 'events/events_list.html', {'events':events})

def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            form.save()
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
    return render(request, 'events/show_venue.html', {'venue':venue})

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
    form = VenueForm(request.POST or None, instance = venue)   
    if request.method == "POST":          
        if form.is_valid():
            form.save()
            return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'form':form})

def add_event(request):
    submitted = False
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            submitted = True
    else:            
        form = EventForm()

    return render(request, 'events/add_event.html', {'form' : form, 'submitted':submitted})

def update_event(request, pk):
    event=get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance = event)   
    if request.method == "POST":          
        if form.is_valid():
            form.save()
            return redirect('list-events')
    return render(request, 'events/update_event.html', {'form':form})

def delete_event(request, pk):
    event=get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('list-events')

def delete_venue(request, pk):
    venue=get_object_or_404(Venue, pk=pk)
    venue.delete()
    return redirect('list-venues')

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

