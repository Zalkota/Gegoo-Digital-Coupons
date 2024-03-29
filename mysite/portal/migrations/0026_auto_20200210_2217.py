# Generated by Django 2.0.8 on 2020-02-10 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0025_followstore'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('FOOD', 'Food'), ('VEHICLES', 'Automotive'), ('HOME', 'Home Improvement'), ('TECH', 'Technology'), ('OFFICE', 'Office'), ('FUN', 'Fun'), ('BEAUTY', 'Beauty'), ('ONLINE', 'Online')], db_index=True, default='FOOD', max_length=20, unique=True),
        ),
    ]
