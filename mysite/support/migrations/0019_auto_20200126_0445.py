# Generated by Django 2.0.8 on 2020-01-26 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0018_auto_20200126_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]
