# Generated by Django 4.0.1 on 2022-01-21 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_playerstatistics_player_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaguesSeasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leagues_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='season', to='api.leagues')),
                ('seasons', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='league', to='api.seasons')),
            ],
        ),
        migrations.RemoveField(
            model_name='teamsleaguesseasons',
            name='leagues_id',
        ),
        migrations.RemoveField(
            model_name='teamsleaguesseasons',
            name='seasons',
        ),
        migrations.RemoveField(
            model_name='teamsleaguesseasons',
            name='team_id',
        ),
        migrations.DeleteModel(
            name='PlayerStatistics',
        ),
        migrations.DeleteModel(
            name='TeamsLeaguesSeasons',
        ),
    ]
