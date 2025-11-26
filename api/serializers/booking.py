from rest_framework import serializers
from api.models import Ticket, Booking

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'name', 'price', 'quantity', 'event', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'ticket', 'user', 'quantity', 'booked_at']