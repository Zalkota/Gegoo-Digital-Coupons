# Generated by Django 2.0.8 on 2020-02-11 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0031_auto_20200211_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=20),
        ),
    ]
