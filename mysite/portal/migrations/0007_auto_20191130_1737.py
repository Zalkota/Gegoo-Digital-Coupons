# Generated by Django 2.0.8 on 2019-11-30 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_remove_about_services_header'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='title',
            field=models.TextField(),
        ),
    ]