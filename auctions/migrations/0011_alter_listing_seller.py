# Generated by Django 4.2.7 on 2023-12-04 02:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]