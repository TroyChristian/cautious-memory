# Generated by Django 4.0.1 on 2022-01-16 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('Buy', 'Buy'), ('Sell', 'Sell'), ('Spend', 'Spend'), ('Acquire', 'Acquire')], default='Buy', max_length=7),
        ),
    ]