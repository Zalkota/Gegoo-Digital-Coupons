# Generated by Django 2.0.8 on 2020-02-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0027_auto_20200210_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=20),
        ),
    ]