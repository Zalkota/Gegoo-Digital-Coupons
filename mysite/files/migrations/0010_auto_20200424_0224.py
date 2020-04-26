# Generated by Django 2.2.10 on 2020-04-24 02:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import files.models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0046_auto_20200423_2158'),
        ('files', '0009_auto_20200311_0000'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(help_text='Image must be a .JPG, PNG, or .JPEG', max_length=255, upload_to=files.models.update_image_filename, validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), files.models.image_size])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('store', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imagefile', to='portal.Store')),
            ],
        ),
        migrations.DeleteModel(
            name='PromotionalVideo',
        ),
    ]