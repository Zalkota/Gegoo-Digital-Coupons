# Generated by Django 2.0.8 on 2019-11-30 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_offer_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategory', to='portal.Subcategory'),
        ),
    ]