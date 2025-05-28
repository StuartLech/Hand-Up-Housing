from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('housing_app', '0008_migrate_listing_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='image3',
        ),
    ]
