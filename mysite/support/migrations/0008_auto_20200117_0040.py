# Generated by Django 2.0.8 on 2020-01-17 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_auto_20200117_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=20),
        ),
    ]
