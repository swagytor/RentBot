from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import viewsets

from events.filters import EventFilter
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import filters


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = EventFilter

    ordering_fields = ['start_date', 'end_date']
    filterset_fields = ['start_date', 'end_date', 'court', 'player']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return Event.objects.filter(end_date__gte=timezone.now())

    @action(methods=['get'], detail=False)
    def my_events(self, request):
        tg_id = self.request.query_params.get('tg_id')

        if tg_id:
            queryset = self.get_queryset().filter(player__tg_id=tg_id)
        else:
            queryset = []
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
