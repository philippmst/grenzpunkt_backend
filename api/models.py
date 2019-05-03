from django.db import models
from django.contrib.auth.models import User


# Create your models here.
CHOICES = {
    'ANGELEGT': 'A', 
    'BEARBEITUNG': 'B',
    'ABGESCHLOSSEN': 'F',
    'GELOESCHT': 'D',
}

STATUS = (
    (CHOICES['ANGELEGT'], 'Angelegt'),
    (CHOICES['BEARBEITUNG'], 'Bearbeitung'),
    (CHOICES['ABGESCHLOSSEN'], 'Abgeschlossen'),
    (CHOICES['GELOESCHT'], 'Geloescht'),
)

class History(models.Model):
    log = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


class Reservierung(models.Model):
    kg = models.CharField('Katastralgemeinde', null=False, blank=False, max_length=5)
    kunde = models.IntegerField(null=False, blank=False)
    # resnr = models.CharField(blank=False, null=False, max_length=25, unique=True)
    history = models.ManyToManyField(History)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=STATUS, default=CHOICES['ANGELEGT'], null=False, blank=False)
    email = models.EmailField(blank=True, null=True)
    planverfasser = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid_to = models.DateField(null=False, blank=False)


class Punkt(models.Model):
    # Können wir die Punktnummer alphanummerisch machen?!?
    kg = models.CharField('Katastralgemeinde', null=False, blank=False, max_length=5)
    reservierung = models.ForeignKey(Reservierung, null=False, blank=False, on_delete=models.DO_NOTHING)
    nummer = models.IntegerField(null=False, blank=False)
    status = models.CharField(max_length=20, default="reserviert")

    class Meta:
        unique_together = ('reservierung', 'nummer')
        ordering: ['nummer']


# class Linie(models.Model):
#     vonPunkt = models.ForeignKey(Punkt, 'vonPunkt', null=False, blank=False, on_delete=models.DO_NOTHING)
#     nachPunkt = models.ForeignKey(Punkt, related_name='nachPunkt', null=False, blank=False, on_delete=models.DO_NOTHING)
