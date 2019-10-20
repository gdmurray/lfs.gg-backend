# Generated by Django 2.2.6 on 2019-10-20 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamleague',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.TeamSettings'),
        ),
        migrations.AddField(
            model_name='leaguerequest',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='league_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaguerequest',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.League'),
        ),
        migrations.AddField(
            model_name='leaguemanagement',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaguemanagement',
            name='league',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leagues.League'),
        ),
        migrations.AddField(
            model_name='leaguemanagement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='league_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='league',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
