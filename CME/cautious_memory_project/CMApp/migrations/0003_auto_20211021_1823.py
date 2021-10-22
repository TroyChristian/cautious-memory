# Generated by Django 3.2.8 on 2021-10-21 18:23

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMApp', '0002_auto_20211021_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='asset_value',
            field=models.DecimalField(decimal_places=8, default=Decimal('0E-8'), max_digits=12),
        ),
        migrations.AddField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='entry',
            name='fiat_value',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12),
        ),
    ]
