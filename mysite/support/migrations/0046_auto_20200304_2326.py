# Generated by Django 2.2.10 on 2020-03-04 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0045_auto_20200229_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=20),
        ),
    ]
