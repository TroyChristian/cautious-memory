# Generated by Django 3.2.8 on 2021-11-16 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMApp', '0014_alter_asset_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='photo',
            field=models.ImageField(default='small.png', upload_to='user_images'),
        ),
    ]
