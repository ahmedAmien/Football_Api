# Generated by Django 4.0.1 on 2022-01-19 08:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_players_first_alter_players_last'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='country_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='players', to='api.countries'),
        ),
    ]
