# Generated by Django 2.0.8 on 2019-01-02 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_delete_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
