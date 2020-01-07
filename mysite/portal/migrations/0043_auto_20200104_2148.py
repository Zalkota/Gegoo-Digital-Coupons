# Generated by Django 2.0.8 on 2020-01-04 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0042_auto_20200104_2028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='store',
        ),
        migrations.AddField(
            model_name='offer',
            name='store',
            field=models.ManyToManyField(related_name='offer', to='portal.Store'),
        ),
    ]
