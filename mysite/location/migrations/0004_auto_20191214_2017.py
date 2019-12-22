# Generated by Django 2.0.8 on 2019-12-14 20:17

import autoslug.fields
import cities_light.abstract_models
import cities_light.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0008_city_timezone'),
        ('location', '0003_auto_20191214_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityCustom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('name_ascii', models.CharField(blank=True, db_index=True, max_length=200)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name_ascii')),
                ('geoname_id', models.IntegerField(blank=True, null=True, unique=True)),
                ('alternate_names', models.TextField(blank=True, default='', null=True)),
                ('display_name', models.CharField(max_length=200)),
                ('search_names', cities_light.abstract_models.ToSearchTextField(blank=True, db_index=True, default='', max_length=4000)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True)),
                ('population', models.BigIntegerField(blank=True, db_index=True, null=True)),
                ('feature_code', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('timezone', models.CharField(blank=True, db_index=True, max_length=40, null=True, validators=[cities_light.validators.timezone_validator])),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region')),
            ],
            options={
                'verbose_name_plural': 'cities',
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='address',
            name='cityCustom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='location.CityCustom'),
        ),
        migrations.AlterUniqueTogether(
            name='citycustom',
            unique_together={('region', 'name'), ('region', 'slug')},
        ),
    ]