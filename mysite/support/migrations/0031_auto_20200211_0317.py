# Generated by Django 2.0.8 on 2020-02-11 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0030_auto_20200211_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('PB', 'Published'), ('DR', 'Draft')], default='DR', max_length=20),
        ),
    ]
