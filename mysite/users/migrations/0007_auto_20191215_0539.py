# Generated by Django 2.0.8 on 2019-12-15 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='merchant_select',
        ),
        migrations.AlterField(
            model_name='profile',
            name='ip_address',
            field=models.CharField(blank=True, default='ABC', max_length=120, null=True),
        ),
    ]
