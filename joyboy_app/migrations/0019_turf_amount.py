# Generated by Django 3.2.8 on 2024-02-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joyboy_app', '0018_remove_turf_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='turf',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
