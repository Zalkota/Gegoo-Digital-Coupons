# Generated by Django 2.2.10 on 2020-03-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0038_auto_20200318_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Approval Required'), (2, 'Published'), (3, 'Denied'), (4, 'Edit Pending'), (5, 'Supscription Required')], default=1),
        ),
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Approval Required'), (2, 'Published'), (3, 'Denied'), (4, 'Edit Pending'), (5, 'Supscription Required')], default=5),
        ),
    ]