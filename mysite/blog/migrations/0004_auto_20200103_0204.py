# Generated by Django 2.0.8 on 2020-01-03 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20191223_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]
