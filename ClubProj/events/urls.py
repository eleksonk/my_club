from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events', views.all_events, name='list-events'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('venues', views.all_venues, name='list-venues'),
    path('venue/<pk>', views.show_venue, name='venue-detail'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('venue/<pk>/update', views.update_venue, name='venue-update'),
    path('add_event', views.add_event, name='add-event'),    
    path('event/<pk>/update', views.update_event, name='event-update'),
    path('event/<pk>/delete', views.delete_event, name='event-delete'),
    path('venue/<pk>/delete', views.delete_venue, name='venue-delete'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    path('my_events', views.my_events, name='my-events'),
    path('search_events', views.search_events, name='search-events'),
    path('admin_approval', views.admin_approval, name='admin-approval'),
    path('venue_events/<venue_id>', views.venue_events, name='venue-events'),
    path('show_event/<event_id>', views.show_event, name='show-event'),
]
