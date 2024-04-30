from rest_framework import viewsets
from events.models import Event
from events.serializers import EventSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import filters


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [filters.OrderingFilter]

    ordering_fields = ['start_date', 'end_date']

    def list(self, request, *args, **kwargs):
        court = self.request.query_params.get('court')
        if court == 'all':
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(court_id=court)
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
