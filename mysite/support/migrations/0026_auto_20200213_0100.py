# Generated by Django 2.0.8 on 2020-02-13 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0025_auto_20200208_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=20),
        ),
    ]
