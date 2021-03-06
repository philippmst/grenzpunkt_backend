# Generated by Django 2.2 on 2019-04-18 07:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_reservierung_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservierung',
            name='resnr',
        ),
        migrations.AddField(
            model_name='reservierung',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservierung',
            name='kg',
            field=models.IntegerField(default=88845, verbose_name='Katastralgemeinde'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservierung',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterUniqueTogether(
            name='punkt',
            unique_together={('reservierung', 'nummer')},
        ),
        migrations.RemoveField(
            model_name='punkt',
            name='kg',
        ),
    ]
