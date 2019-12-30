# Generated by Django 2.0.8 on 2019-12-30 04:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=36)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('position', models.PositiveSmallIntegerField(null=True)),
                ('membership_type', models.CharField(choices=[('BM', 'Basic Advertising'), ('PM', 'Premium Advertising')], default='Basic Advertising', max_length=30)),
                ('description', models.CharField(default='add description', max_length=255)),
                ('price', models.PositiveIntegerField(default=0)),
                ('stripe_price', models.PositiveIntegerField(default=0)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('stripe_plan_id', models.CharField(max_length=40)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('benefit', models.ManyToManyField(to='memberships.Benefit')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(editable=False, max_length=7, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=6, null=True)),
                ('success', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('subscription', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscription_transaction', to='memberships.Subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_transaction', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='membership', to='memberships.Membership')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_membership', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subscription',
            name='user_membership',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_membership', to='memberships.UserMembership'),
        ),
    ]
