# Generated by Django 2.0.8 on 2020-01-25 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0014_auto_20200124_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('PB', 'Published'), ('DR', 'Draft')], default='DR', max_length=20),
        ),
    ]
