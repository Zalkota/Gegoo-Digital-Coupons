# Generated by Django 2.0.8 on 2019-05-26 22:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0051_auto_20190521_0145'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermembership',
            name='stripe_customer_id',
        ),
    ]