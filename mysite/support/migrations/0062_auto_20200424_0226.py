# Generated by Django 2.2.10 on 2020-04-24 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0061_auto_20200423_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=20),
        ),
    ]
