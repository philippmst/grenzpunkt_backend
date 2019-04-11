from django.shortcuts import render
from django.contrib.auth.models import User
from api.models import Reservierung, Punkt
from api.serializers import ReservierungSerializer, PunktSerializer, AddPunktSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, action
import json
# from api.utils import ServiceUnavailable, get_database_connection, connected_only



class ReservierungViewSet(viewsets.ModelViewSet):
    queryset = Reservierung.objects.all()
    serializer_class = ReservierungSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'options', 'head', 'post', 'delete' ]

    # def initial(self, request, *args, **kwargs):
    #     x = get_database_connection(False)
    #     x = get_database_connection(True)
    #     self.connection = x
    #     super(ReservierungViewSet, self).initial(request, *args, **kwargs)


    # def get_queryset(self):
    #     res = self.queryset
    #     return res

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        serializer.save(user=User.objects.first())


    @action(detail=True, methods=['post'])
    def add_gpkt(self, request, pk=None):
        res = self.get_object()
        serializer = AddPunktSerializer(data=request.data)
        if serializer.is_valid():
            kg = serializer.data['kg']
            point_nums = serializer.data['point_nums']
            max_num = Punkt.objects.filter(kg=kg).order_by('-nummer').first().nummer+1
            print(max_num)
            for i in range(int(point_nums)):
                p = Punkt(reservierung=res, kg=kg, nummer=max_num+i)
                p.save()
            s = ReservierungSerializer(res, context={'request': request})
            
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # @action(detail=True, methods=['delete'])
    # def del_gpkt(self, request, pk=None):
    #     if self.connection:
    #         pass
    #     raise ServiceUnavailable


    # def destroy(self, request, pk=None):
    #     # Löschen der Reservierung darf nur passieren, wenn noch kein Grenzpunkt angemerkt ist.
    #     pass


    # @connected_only
    # def update(self, request, pk=None):
    #     detail = {'detail': 'Method "PUT" not allowed.'}
    #     return Response(detail, status=status.HTTP_405_METHOD_NOT_ALLOWED)



class PunktViewSet(viewsets.ModelViewSet):
    queryset = Punkt.objects.all()
    serializer_class = PunktSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'options', 'head', 'post', 'delete' ]
