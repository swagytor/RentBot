import django_filters

from events.models import Event


class EventFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='start_date', lookup_expr='date')
    end_date = django_filters.DateFilter(field_name='end_date', lookup_expr='date')

    class Meta:
        model = Event
        fields = '__all__'

