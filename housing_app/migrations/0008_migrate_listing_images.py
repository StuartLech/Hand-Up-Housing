from django.db import migrations


def forwards(apps, schema_editor):
    Listing = apps.get_model('housing_app', 'Listing')
    ListingImage = apps.get_model('housing_app', 'ListingImage')
    db_alias = schema_editor.connection.alias
    for listing in Listing.objects.using(db_alias).all():
        for field in ['image1', 'image2', 'image3']:
            image = getattr(listing, field, None)
            if image:
                ListingImage.objects.using(db_alias).create(listing_id=listing.id, image=image)

def backwards(apps, schema_editor):
    Listing = apps.get_model('housing_app', 'Listing')
    ListingImage = apps.get_model('housing_app', 'ListingImage')
    db_alias = schema_editor.connection.alias
    for img in ListingImage.objects.using(db_alias).all():
        listing = Listing.objects.using(db_alias).get(id=img.listing_id)
        # find first empty slot among image1, image2, image3
        for field in ['image1', 'image2', 'image3']:
            if not getattr(listing, field):
                setattr(listing, field, img.image)
                listing.save(update_fields=[field])
                break

class Migration(migrations.Migration):
    dependencies = [
        ('housing_app', '0007_create_listingimage'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
