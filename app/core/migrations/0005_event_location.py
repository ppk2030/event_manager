# Generated by Django 4.0.10 on 2023-06-20 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_capacity_event_maximum_capacity_event_mode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
