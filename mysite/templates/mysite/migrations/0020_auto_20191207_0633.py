# Generated by Django 2.0.8 on 2019-12-07 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20191206_0411'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='video_url',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='merchant',
            name='ref_code',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True),
        ),
    ]