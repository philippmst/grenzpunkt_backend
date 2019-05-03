from django.shortcuts import render
from django.contrib.auth.models import User
from api.models import Reservierung, Punkt, CHOICES, History
from api.serializers import ReservierungSerializer, PunktSerializer, AddPunktSerializer, AddPunktNrSerializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, action
import json
import logging
logger = logging.getLogger('django')
from api.findnumber import findnumber
from django.core.mail import send_mail
from django.db.models import Q

# from api.utils import ServiceUnavailable, get_database_connection, connected_only
def checkInt(x):
    try:
        int(x)
        return True
    except:
        return False


class ReservierungViewSet(viewsets.ModelViewSet):
    queryset = Reservierung.objects.all()
    serializer_class = ReservierungSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get', 'options', 'head', 'post', 'delete', 'put',]


    def add_history(self, msg):
        h = History(log=msg, user=User.objects.first())
        h.save()
        res = self.get_object()
        res.history.add(h)


    def get_queryset(self):
        queryset = self.queryset
        filtername = self.request.query_params.get('filterByName', None)

        if filtername is not None:
            if checkInt(filtername):
                queryset = queryset.filter(Q(kg__icontains=filtername) | Q(planverfasser__contains=filtername) | Q(kunde=int(filtername)))
            else:
                queryset = queryset.filter(Q(kg__icontains=filtername) | Q(planverfasser__contains=filtername))
        return queryset.order_by('-id')

        
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

            nums = findnumber(point_array, point_nums)
            for i in nums:
                p = Punkt(reservierung=res, kg=kg, nummer=i)
                p.save()
            # logger.info("{} Punkte wurden geadded! - INFO".format(point_nums))
            self.add_history(msg="Punkte hinzugefügt: {}".format(", ".join([str(n) for n in nums])))
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

            self.add_history(msg="Punkte hinzugefügt: {}".format(point_vals))
            
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
            self.add_history(msg="Status wurde auf BEARBEITUNG verändert")

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
            self.add_history(msg="Status wurde auf ABGESCHLOSSEN verändert")
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
        print("points <<{}>>".format(points))
        if points:
            delpoints = []
            for p in points.split(','):
                point = res.punkt_set.filter(nummer=p)
                if point:
                    delpoints.append(point[0].nummer)
                    point[0].delete()
            
            self.add_history(msg="Punkte gelöscht: {}".format(points))
            s = ReservierungSerializer(res, context={'request': request})
            nd = {'delpoints':delpoints}
            nd.update(s.data)
            return Response(nd, status=status.HTTP_200_OK)

        error = "Es wurden keine Punktnummern übergeben."
        return Response(data=error, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['post'])
    def send_mail(self, request, pk=None):
        res = self.get_object()
        subject = "Reservierung Nr. {}, KG {}".format(res.id, res.kg)
        punkte = " ".join(['<li>'+str(p.nummer)+'</li>' for p in res.punkt_set.all()])
        message = "In der Katastralgemeinde<br>{kg}<br>wurden folgende Punktnummern:<br><ul> {punkte}</ul><br> für sie reserviert".format(kg=res.kg,punkte=punkte)
        try:
            send_mail(subject, message, 'noreply@ovg.at', [res.email], html_message=message)
        except :
            return Response(data='Zustellung nicht möglich', status=status.HTTP_400_BAD_REQUEST)
        return Response(data='Zustellung erfolgt', status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        res = self.get_object()
        if res.status is not CHOICES['ANGELEGT']:
            error = "Punkte dieser Reservierung sind bereits in Bearbeitung. Löschen nicht mehr möglich."
            return Response(data=error, status=status.HTTP_400_BAD_REQUEST)
        else:
            for p in res.punkt_set.all():
                p.delete()
            msg = "die Reservierung mit der Nummer: {} wurde gelöscht".format(res.id)
            self.add_history(msg="Reservierung gelöscht")
            res.status = 'D'
            res.save()
            return Response(data=msg, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        detail = {'detail': 'Method "PUT" not allowed.'}
        return Response(detail, status=status.HTTP_405_METHOD_NOT_ALLOWED)

