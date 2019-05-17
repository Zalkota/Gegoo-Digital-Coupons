# Generated by Django 2.0.8 on 2019-05-01 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0038_course_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(db_index=True, default=True, help_text='Designates whether this item should be treated as active. Unselect this instead of deleting data.')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='last modified time')),
                ('first_name', models.CharField(help_text='First name', max_length=50)),
                ('last_name', models.CharField(help_text='Last name', max_length=50)),
                ('company', models.CharField(help_text='Company', max_length=50)),
                ('email', models.CharField(help_text='Email', max_length=50)),
                ('appointment_time', models.PositiveSmallIntegerField(choices=[(1, '3:00pm'), (2, '3:45pm'), (3, '4:30pm'), (4, '5:15pm'), (5, '6:00pm'), (6, '6:45pm')], db_index=True, default=None, verbose_name='Rate this course between 1-5 stars.')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
