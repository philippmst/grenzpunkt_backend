from django.shortcuts import render
from django.contrib.auth.models import User
from api.models import Reservierung, Punkt, CHOICES
from api.serializers import ReservierungSerializer, PunktSerializer, AddPunktSerializer, AddPunktNrSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, action
import json
import logging
logger = logging.getLogger('django')
from api.findnumber import findnumber

# from api.utils import ServiceUnavailable, get_database_connection, connected_only



class KGViewSet(viewsets.ModelViewSet):
    queryset = Katastralgemeinde.objects.all()
    serializer_class = ReservierungSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'options', 'head', 'post', 'delete', 'put',]


    def get_queryset(self):
        res = self.queryset
        return res

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
            KgPoints = Punkt.objects.filter(kg=kg)
            if not KgPoints:
                point_array = [0]
            else:
                point_array = [p.nummer for p in KgPoints]

            for i in findnumber(point_array, point_nums):
                p = Punkt(reservierung=res, kg=kg, nummer=i)
                p.save()
            logger.info("{} Punkte wurden geadded! - INFO".format(point_nums))
            s = ReservierungSerializer(res, context={'request': request})
            
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def add_gpkt_nr(self, request, pk=None):
        res = self.get_object()
        serializer = AddPunktNrSerializer(data=request.data)
        if serializer.is_valid():
            kg = serializer.data['kg']
            point_vals = serializer.data['point_vals']
            KgPoints = Punkt.objects.filter(kg=kg)
            # check if all pointNumbers are integers, and the numbers are available
            for p in point_vals.split(','):
                try:
                    pp = int(p)
                    if KgPoints.filter(nummer=pp):
                        error = '{} ist bereits vergeben'.format(pp)
                        return Response(data=error, status=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    error = '{} ist keine gültige Punktnummer'.format(p)
                    return Response(data=error, status=status.HTTP_406_NOT_ACCEPTABLE)

            # if all valid numbers -> then save
            for p in point_vals.split(','):
                pu = Punkt(reservierung=res, kg=kg, nummer=int(p))
                pu.save()
            s = ReservierungSerializer(res, context={'request': request})
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['put'])
    def set_progress(self, request, pk=None):
        # das passiert sobald der Plan eingetroffen ist
        # und die Nummern jetzt in der Vordurchführungsebene sind.
        res = self.get_object()
        if res.status == CHOICES['ANGELEGT']:
            res.status = CHOICES['BEARBEITUNG']
            res.save()
            s = ReservierungSerializer(res, context={'request': request})
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            error = 'Der Status der Reservierung darf nicht mehr verändert werden'
            return Response(data=error, status=status.HTTP_403_FORBIDDEN)
           
    @action(detail=True, methods=['put'])
    def set_done(self, request, pk=None):
        # Nummern sind rechtskräftig.
        res = self.get_object()
        if res.status == CHOICES['BEARBEITUNG']:
            res.status = CHOICES['ABGESCHLOSSEN']
            res.save()
            s = ReservierungSerializer(res, context={'request': request})
            return Response(data=s.data, status=status.HTTP_200_OK)
        else:
            error = 'Der Status der Reservierung darf nicht mehr verändert werden'
            return Response(data=error, status=status.HTTP_403_FORBIDDEN)




    @action(detail=True, methods=['post'])
    def del_gpkt(self, request, pk=None):
        res = self.get_object()
        if res.status == CHOICES['ABGESCHLOSSEN']:
            error = 'Grenzpunkte dürfen nicht mehr verändert werden.'
            return Response(data=error, status=status.HTTP_403_FORBIDDEN)

        points = request.data['points']
        if points:
            delpoints = 0
            for p in points.split(','):
                point = Punkt.objects.filter(nummer=p)
                if point:
                    point[0].delete()
                    delpoints += 1
            
            s = ReservierungSerializer(res, context={'request': request})
            nd = {'delpoints':delpoints}
            nd.update(s.data)
            return Response(nd, status=status.HTTP_200_OK)

        error = "Es wurden keine Punktnummern übergeben."
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)



    def destroy(self, request, pk=None):
        res = self.get_object()
        if res.status is not CHOICES['ANGELEGT']:
            error = "Punkte dieser Reservierung sind bereits in Bearbeitung. Löschen nicht mehr möglich."
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
        else:
            for p in res.punkt_set.all():
                p.delete()
            msg = "die Reservierung mit der Nummer: {} wurde gelöscht".format(res.id)
            res.delete()
            return Response(data=msg, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        detail = {'detail': 'Method "PUT" not allowed.'}
        return Response(detail, status=status.HTTP_405_METHOD_NOT_ALLOWED)

