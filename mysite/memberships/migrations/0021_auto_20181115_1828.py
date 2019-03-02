# Generated by Django 2.0.8 on 2018-11-15 18:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0020_auto_20181115_0328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='id',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='order_id',
            field=models.CharField(blank=True, default=uuid.uuid4, editable=False, max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
