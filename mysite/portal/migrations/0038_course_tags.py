# Generated by Django 2.0.8 on 2019-01-31 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0037_auto_20190126_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tags',
            field=models.CharField(default='course', help_text='Write keywords that describe this course, this helps the websites search engine. Lower case words and include title of course.', max_length=100),
        ),
    ]
