from rest_framework import serializers
from api.models import Event, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category',
            'start_time', 'end_time',
            'created_at', 'update_at'
        ]
        read_only_fields = ['created_at', 'update_at']