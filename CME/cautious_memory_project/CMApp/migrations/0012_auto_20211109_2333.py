# Generated by Django 3.2.8 on 2021-11-09 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CMApp', '0011_alter_asset_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='image_height',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='image_width',
        ),
        migrations.AlterField(
            model_name='asset',
            name='photo',
            field=models.ImageField(blank=True, default='small.png', height_field='100', help_text='Asset Image', null=True, upload_to='media', verbose_name='Asset Image', width_field='100'),
        ),
    ]
