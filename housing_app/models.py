from django.db import models

PROPERTY_TYPES = (
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('condo', 'Condo'),
)

YES_NO_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

class Listing(models.Model):
    address = models.CharField(max_length=255)
    landlord_contact = models.CharField(max_length=255, blank=True, null=True)

    # Filters
    bedrooms = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES, default='house')
    pets_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    ada_accessible = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    income_requirement = models.CharField(max_length=255, blank=True, null=True)
    past_eviction_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    sex_offender_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    criminal_record_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    issues_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)

    # OPTIONAL: Additional fields if you want them
    additional_info = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address} ({self.property_type})"

