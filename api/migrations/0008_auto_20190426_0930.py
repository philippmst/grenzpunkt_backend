# Generated by Django 2.2 on 2019-04-26 09:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20190425_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservierung',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='reservierung',
            name='planverfasser',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='reservierung',
            name='valid_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
