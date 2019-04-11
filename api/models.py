from django.db import models
from django.contrib.auth.models import *

# Create your models here.


class Reservierung(models.Model):
    resnr = models.CharField(blank=False, null=False, max_length=25, unique=True)
    kunde = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Punkt(models.Model):
    reservierung = models.ForeignKey(Reservierung, null=False, blank=False, on_delete=models.DO_NOTHING)
    kg = models.IntegerField('Katastralgemeinde', null=False, blank=False)
    nummer = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=20, default="reserviert")
    # Können wir die Punktnummer alphanummerisch machen?!?

    class Meta:
        unique_together = ('kg', 'nummer')


class Linie(models.Model):
    vonPunkt = models.ForeignKey(Punkt, 'vonPunkt', null=False, blank=False, on_delete=models.DO_NOTHING)
    nachPunkt = models.ForeignKey(Punkt, related_name='nachPunkt', null=False, blank=False, on_delete=models.DO_NOTHING)
    