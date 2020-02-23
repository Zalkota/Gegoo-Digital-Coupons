# Generated by Django 2.2.10 on 2020-02-23 22:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0024_auto_20200209_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('ALL', 'All Services'), ('AUTO', 'Auto'), ('BEAUTY', 'Beauty'), ('COMMUNITY', 'Community'), ('CONSTRUCTION', 'Construction'), ('FOOD', 'Food'), ('FUN', 'Fun'), ('GARDEN', 'Garden'), ('GROCERIES', 'Groceries'), ('HEALTH', 'Health'), ('HOME', 'Home Improvement'), ('PETS', 'Pets'), ('RETAIL', 'Retail')], db_index=True, default='FOOD', max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Being Reviewed'), (2, 'Published'), (3, 'Denied')], default=1),
        ),
        migrations.AlterField(
            model_name='store',
            name='logo',
            field=models.ImageField(null=True, upload_to='store-logos/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.PositiveIntegerField(choices=[(1, 'Being Reviewed'), (2, 'Published'), (3, 'Denied')], default=1),
        ),
    ]
