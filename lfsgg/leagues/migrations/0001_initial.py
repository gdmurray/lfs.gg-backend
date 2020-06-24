# Generated by Django 2.2.6 on 2019-11-19 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('logo', models.FileField(null=True, upload_to='')),
                ('url', models.URLField(max_length=250, null=True)),
                ('official', models.BooleanField(default=False)),
                ('open', models.BooleanField(default=True)),
                ('user_created', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueManagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('OWNER', 'Owner'), ('USER', 'User'), ('PLAYER', 'Player')], default='USER', max_length=10)),
                ('status', models.CharField(choices=[('APPLIED', 'Applied'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined'), ('CREATED', 'Created')], default='APPLIED', max_length=12)),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(blank=True, null=True)),
                ('approved_notes', models.TextField(blank=True, max_length=1000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('APPLIED', 'Applied'), ('APPROVED', 'Approved'), ('DECLINED', 'Declined')], default='APPLIED', max_length=15)),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(null=True)),
                ('approved_notes', models.TextField(blank=True, max_length=1000, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeagueSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TeamLeague',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='league_user_approved_by', to=settings.AUTH_USER_MODEL)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='leagues.League')),
            ],
        ),
    ]
