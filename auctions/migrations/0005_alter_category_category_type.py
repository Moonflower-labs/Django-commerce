# Generated by Django 4.2.7 on 2023-11-30 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(choices=[('', 'Select a Category'), ('FA', 'Fashion'), ('KI', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), ('BO', 'Books'), ('TO', 'Tools')], max_length=2),
        ),
    ]
