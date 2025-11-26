from rest_framework import serializers
from api.models import Event, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M",
        input_formats=["%Y-%m-%dT%H:%M"],
        required=True
    )
    end_time = serializers.DateTimeField(
        format="%Y-%m-%dT%H:%M",
        input_formats=["%Y-%m-%dT%H:%M"],
        required=True
    )

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'category',
            'start_time', 'end_time',
            'created_at', 'update_at'
        ]
