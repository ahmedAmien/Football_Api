# Generated by Django 4.0.1 on 2022-01-21 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_playerstatistics_player_id_teamsleaguesseasons_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerstatistics',
            name='player_id',
        ),
    ]
