# Generated by Django 2.2.10 on 2020-03-29 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0040_auto_20200329_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Draft'), (2, 'Published'), (3, 'Denied')], default=3),
        ),
    ]