# Generated by Django 2.2 on 2019-04-26 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20190426_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservierung',
            name='valid_to',
            field=models.DateField(),
        ),
    ]
