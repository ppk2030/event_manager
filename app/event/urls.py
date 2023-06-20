"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
)

from event import views

app_name = 'event'

urlpatterns = [
    path('list/', views.ListEventView.as_view(), name='event-list'),
    path('create/', views.CreateEventView.as_view(), name='event-create'),
    path('<int:pk>/', views.ManageEventView.as_view(), name='event-update'),

    #Tickets or all events for a specific user
    path('booking/', views.BookTicketList.as_view(), name='booking-list'),

    # Book Tickets for an event for a specific user
    path('booking/create/', views.BookTicketView.as_view(), name='booking-create'),
]