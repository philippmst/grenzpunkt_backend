from rest_framework import serializers
from api.models import Punkt, Reservierung, History



class SmallPunktSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Punkt
        ordering = ('nummer')
        fields = ('url', 'id',)


class PunktSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Punkt
        fields = ('kg', 'nummer', 'status', 'id') 
        ordering = ('nummer')


class HistorySerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = History
        fields = ('log', 'created_at', 'username')


class ReservierungSerializer(serializers.HyperlinkedModelSerializer):
    # history = serializers.PrimaryKeyRelatedField(many=True, queryset=History.objects.all() )
    history = HistorySerializer(many=True, read_only=True)
    punkt_set = PunktSerializer(many=True, required=False)   
    class Meta:
        model = Reservierung
        fields = ('kg', 'kunde', 'id', 'punkt_set', 'status', 'created_at', 'updated_at', 'valid_to', 'planverfasser', 'email', 'url', 'history')


class AddPunktSerializer(serializers.Serializer):
    kg = serializers.IntegerField()
    point_nums = serializers.IntegerField()


class AddPunktNrSerializer(serializers.Serializer):
    kg = serializers.IntegerField()
    point_vals = serializers.CharField()
