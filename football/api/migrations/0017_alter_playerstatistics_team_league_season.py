# Generated by Django 4.0.1 on 2022-01-21 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_players_team_id_teamsplayersleaguesseasons_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerstatistics',
            name='team_league_season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='player_statistics', to='api.teamsplayersleaguesseasons'),
        ),
    ]