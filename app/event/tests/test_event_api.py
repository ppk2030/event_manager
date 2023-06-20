"""
Tests for event APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Event

from event.serializers import EventSerializer


EVENTS_URL = reverse('event:event-list')
CREATE_URL = reverse('event:event-create')


def detail_url(event):
    """Create and return a recipe detail URL."""
    return reverse('event:event-update', kwargs={'pk': event.id})


def create_event(user, **params):
    """Create and return a sample event."""
    defaults = {
        'title': 'Sample event name',
        'time_minutes': 5,
        'price': Decimal('5.50'),
        'description': 'Sample event description.',
        'maximum_capacity': 45,
        'link': 'http://example.com/event.pdf',
        "total_booking": 0,
        "mode": "online",
        "location": "India"
    }

    defaults.update(params)

    event = Event.objects.create(user=user, **defaults)
    return event


class PublicEventAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(EVENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateEventApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_events(self):
        """Test retrieving a list of events."""
        create_event(user=self.user)
        create_event(user=self.user)

        res = self.client.get(EVENTS_URL)
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AdminEventApiTests(TestCase):
    """Test authenticated Admin API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_get_event_detail(self):
        """Test get event detail."""
        event = create_event(user=self.user)
        url = detail_url(event)
        res = self.client.get(url)

        serializer = EventSerializer(event)

        self.assertEqual(res.data, serializer.data)

    def test_create_event(self):
        """Test creating an event."""

        payload = {
            'title': 'Sample event name',
            'time_minutes': 5,
            'price': Decimal('5.50'),
            'description': 'Sample event description.',
            'maximum_capacity': 45,
            'link': 'http://example.com/event.pdf',
        }
        res = self.client.post(CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        event = Event.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(event, k), v)
        self.assertEqual(event.user, self.user)

    def test_partial_update(self):
        """Test partial update of an event."""
        original_link = 'https://example.com/event.pdf'
        event = create_event(
            user=self.user,
            title='Sample event title',
            link=original_link,
            time_minutes=400,
            price=700,
            maximum_capacity=100
        )

        payload = {'title': 'New event title'}
        url = detail_url(event
                         )
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        self.assertEqual(event.title, payload['title'])
        self.assertEqual(event.link, original_link)
        self.assertEqual(event.user, self.user)

    def test_full_update(self):
        """Test full update of event."""
        event = create_event(
            user=self.user,
            title='Sample event title',
            link='https://example.com/event.pdf',
            time_minutes=400,
            price=700,
            maximum_capacity=100
        )

        payload = {
            'title': 'New event title',
            'link': 'https://examples.com/new-event.pdf',
            'description': 'New event description',
            'time_minutes': 10,
            'price': Decimal('2.50'),
            'maximum_capacity': 45,
        }
        url = detail_url(event)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        event.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(event, k), v)
        self.assertEqual(event.user, self.user)

    def test_delete_event(self):
        """Test deleting a event successful."""
        event = create_event(user=self.user)

        url = detail_url(event)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    # def test_events_list_limited_to_user(self):
    #     """Test list of events is limited to authenticated user."""
    #     other_user = get_user_model().objects.create_user(
    #         'other@example.com',
    #         'password123',
    #     )
    #     create_event(user=other_user)
    #     create_event(user=self.user)
    #
    #     res = self.client.get(EVENTS_URL)
    #
    #     events = Event.objects.filter(user=self.user)
    #     serializer = EventSerializer(events, many=True)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)
