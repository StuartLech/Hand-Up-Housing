# Generated by Django 4.1.5 on 2025-02-10 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('housing_app', '0002_listing_additional_info_listing_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='income_requirement',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
