# Generated by Django 4.0.1 on 2022-01-21 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_players_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='injured',
            field=models.BooleanField(default=False),
        ),
    ]
