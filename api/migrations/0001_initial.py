# Generated by Django 2.2 on 2019-04-11 19:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservierung',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resnr', models.CharField(editable=False, max_length=25, unique=True)),
                ('kunde', models.IntegerField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Punkt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kg', models.IntegerField(editable=False, verbose_name='Katastralgemeinde')),
                ('nummer', models.IntegerField(editable=False)),
                ('reservierung', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Reservierung')),
            ],
            options={
                'unique_together': {('kg', 'nummer')},
            },
        ),
    ]