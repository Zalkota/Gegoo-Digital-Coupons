# Generated by Django 2.0.8 on 2019-02-24 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0034_auto_20190224_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='benefit',
            field=models.ManyToManyField(to='memberships.Benefit'),
        ),
    ]
