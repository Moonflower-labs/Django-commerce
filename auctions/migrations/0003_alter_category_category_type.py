# Generated by Django 4.2.7 on 2023-11-30 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_watchlist_comment_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(choices=[(None, 'Select a Category'), ('FA', 'Fashion'), ('KI', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), ('BO', 'Books'), ('TO', 'Tools')], max_length=2),
        ),
    ]
