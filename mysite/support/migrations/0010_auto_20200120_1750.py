# Generated by Django 2.0.8 on 2020-01-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0009_auto_20200119_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=20),
        ),
    ]
