from rest_framework import serializers
from api.models import Punkt, Reservierung





class PunktSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Punkt
        fields = '__all__' 


class ReservierungSerializer(serializers.HyperlinkedModelSerializer):
    punkt_set = PunktSerializer(many=True, required=False)    
    class Meta:
        model = Reservierung
        exclude = ('user',)


class AddPunktSerializer(serializers.Serializer):
    kg = serializers.IntegerField()
    point_nums = serializers.IntegerField()