# Generated by Django 2.0.8 on 2020-01-19 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0008_auto_20200119_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]