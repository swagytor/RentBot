from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    end_date = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    _court = serializers.SlugRelatedField(slug_field="title", read_only=True, source="court")
    _player = serializers.SlugRelatedField(slug_field="name", read_only=True, source="player")

    class Meta:
        model = Event
        fields = "__all__"
