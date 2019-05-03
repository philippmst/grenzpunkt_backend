from api.models import Punkt
from api.serializers import PunktSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, action



class PunktViewSet(viewsets.ModelViewSet):
    queryset = Punkt.objects.all()
    serializer_class = PunktSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'options', 'head', 'post', 'delete' ]

    def get_queryset(self):
        return self.queryset.order_by('-nummer')
