# Generated by Django 2.2 on 2019-04-11 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='punkt',
            name='status',
            field=models.CharField(default='reserviert', max_length=20),
        ),
        migrations.AlterField(
            model_name='punkt',
            name='kg',
            field=models.IntegerField(verbose_name='Katastralgemeinde'),
        ),
        migrations.AlterField(
            model_name='punkt',
            name='nummer',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reservierung',
            name='kunde',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reservierung',
            name='resnr',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
