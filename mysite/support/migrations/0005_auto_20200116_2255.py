# Generated by Django 2.0.8 on 2020-01-16 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_auto_20200116_0326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=20),
        ),
    ]