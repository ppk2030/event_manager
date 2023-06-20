"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Event, Booking


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for booking."""
    event_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Booking
        fields = ['event_user', 'event', 'quantity']
        read_only_fields = ['event_user']
        extra_kwargs = {"quantity": {"error_messages": {"blank": "Booking exceeding capacity"}}}

    def create(self, validated_data):
        user = self.context['request'].user

        event = validated_data.get('event', None)
        quantity = validated_data.get('quantity', None)

        maximum_capacity = Event.objects.filter(id=event.id)[0].maximum_capacity
        total_booking = Event.objects.filter(id=event.id)[0].total_booking

        existing_quantity = Booking.objects.filter(event_user=user, event=event)
        if existing_quantity:
            existing_quantity = existing_quantity[0].quantity
        else:
            existing_quantity = 0
        final_quantity = quantity+existing_quantity

        total_booking = total_booking + quantity
        Event.objects.filter(id=event.id).update(total_booking=total_booking)

        if (total_booking + quantity) > maximum_capacity:
            booking = Booking.objects.get(event_user=user, event=event)
        else:
            updated_values = {'quantity': final_quantity}
            booking, created = Booking.objects.update_or_create(event_user=user, event=event, defaults=updated_values)

        return booking


class BookingDetailSerializer(serializers.ModelSerializer):
    """Serializer for booking Detail"""
    event_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    title = serializers.CharField(source='event.title')
    date = serializers.DateTimeField(source='event.date')
    duration = serializers.IntegerField(source='event.time_minutes')
    location = serializers.CharField(source='event.location')

    class Meta:
        model = Booking
        fields = ['event_user', 'event', 'quantity', 'title', 'date', 'duration', 'location']
        read_only_fields = ['event_user']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for event."""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    booking = BookingSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ['user', 'title', 'description', 'time_minutes', 'date', 'price', 'maximum_capacity', 'link', 'id',
                  'booking', 'total_booking', 'mode']
        read_only_fields = ['id', 'user']
