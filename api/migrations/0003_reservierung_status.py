# Generated by Django 2.2 on 2019-04-12 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190411_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservierung',
            name='status',
            field=models.CharField(choices=[('A', 'Angelegt'), ('B', 'Bearbeitung'), ('F', 'Abgeschlossen')], default='A', max_length=1),
        ),
    ]