# Generated by Django 2.0.8 on 2020-01-26 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0017_auto_20200126_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=20),
        ),
    ]