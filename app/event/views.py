from django.shortcuts import render
"""
Views for the event APIs
"""

from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.
from core.models import Event, Booking
from event.serializers import EventSerializer, BookingSerializer, BookingDetailSerializer


class ListEventView(generics.ListAPIView):
    """
    View to list all events in the system.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('title')
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class CreateEventView(generics.CreateAPIView):
    """Create a new event in the system."""
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class ManageEventView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the created event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Event.objects.filter(id=pk)


class BookTicketList(generics.ListAPIView):
    """
    View to list all booked ticket for a particular user in the system.
    """
    serializer_class = BookingDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(event_user=user)

class BookTicketView(generics.CreateAPIView):
    """Create a new event in the system."""
    serializer_class = BookingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        event = self.request.data['event']
        quantity =self.request.data['quantity']
        return Booking.objects.filter(event=event, event_user=user, quantity=quantity)



