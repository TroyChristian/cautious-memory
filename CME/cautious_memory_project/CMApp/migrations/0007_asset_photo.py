# Generated by Django 3.2.8 on 2021-11-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMApp', '0006_alter_portfolio_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='photo',
            field=models.ImageField(default='btc_default.jpg', upload_to=''),
        ),
    ]
