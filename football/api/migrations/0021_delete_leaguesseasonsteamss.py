# Generated by Django 4.0.1 on 2022-01-21 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_remove_leaguesseasonsteamss_team_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LeaguesSeasonsTeamss',
        ),
    ]
