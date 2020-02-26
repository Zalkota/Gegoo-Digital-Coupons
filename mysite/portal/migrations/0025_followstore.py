# Generated by Django 2.0.8 on 2020-02-05 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0024_auto_20200204_0207'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connections', models.ManyToManyField(to='portal.Store')),
                ('current_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]