# Generated by Django 2.0.8 on 2020-02-20 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0038_auto_20200219_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('PB', 'Published'), ('DR', 'Draft')], default='DR', max_length=20),
        ),
    ]