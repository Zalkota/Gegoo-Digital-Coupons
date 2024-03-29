# Generated by Django 2.0.8 on 2019-12-17 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0034_auto_20191214_2000'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=100)),
                ('context', models.CharField(choices=[('A', 'Accounts'), ('B', 'Billing'), ('GS', 'Getting Started'), ('P', 'Payments'), ('V', 'Verification')], max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]
