from rest_framework import viewsets
from courts.models import Court
from courts.serializers import CourtSerializer

class CourtViewSet(viewsets.ModelViewSet):
    queryset = Court.objects.all()
    serializer_class = CourtSerializer
