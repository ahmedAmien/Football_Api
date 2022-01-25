# Generated by Django 4.0.1 on 2022-01-21 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_leaguesseasonsteamss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaguesseasonsteamss',
            name='team_id',
        ),
        migrations.AddField(
            model_name='leaguesseasonsteamss',
            name='team_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='leaguess', to='api.teams'),
        ),
    ]