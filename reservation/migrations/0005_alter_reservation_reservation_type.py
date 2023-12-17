# Generated by Django 5.0 on 2023-12-17 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_remove_reservation_lodging_reservation_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='reservation_type',
            field=models.CharField(choices=[('RO', 'Room'), ('TR', 'Train'), ('BU', 'Bus'), ('RC', 'Rental Car')], max_length=100),
        ),
    ]
