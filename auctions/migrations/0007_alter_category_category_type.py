# Generated by Django 4.2.7 on 2023-11-30 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_category_category_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_type',
            field=models.CharField(blank=True, choices=[(None, 'Select a Category'), ('FA', 'Fashion'), ('KI', 'Toys'), ('EL', 'Electronics'), ('HO', 'Home'), ('BO', 'Books'), ('TO', 'Tools'), ('ED', 'Edibles')], max_length=2),
        ),
    ]
