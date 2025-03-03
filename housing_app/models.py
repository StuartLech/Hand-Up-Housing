from django.db import models

PROPERTY_TYPES = (
    ('house', 'House'),
    ('apartment', 'Apartment'),
    ('condo', 'Condo'),
    ('group_home', 'Group Home'),  # New type
)

YES_NO_CHOICES = (
    (True, 'Yes'),
    (False, 'No'),
)

# Criminal record choices
CRIMINAL_RECORD_CHOICES = (
    ('none', 'None Allowed (Clear Record Only)'),
    ('misdemeanor', 'Misdemeanor Allowed (Per Review)'),
    ('felony', 'Felony Allowed (Per Review)'),
)

# Income requirement choices
INCOME_CHOICES = (
    ('under_20', 'Under $20,000'),
    ('30_40', '$30,000-$40,000'),
    ('40_50', '$40,000-$50,000'),
    ('50_plus', '$50,000 and Above'),
)

class Listing(models.Model):
    # Separated address
    street = models.CharField(max_length=255, blank=True, null=True)
    city   = models.CharField(max_length=100, blank=True, null=True)
    state  = models.CharField(max_length=50, blank=True, null=True)
    zip    = models.CharField(max_length=20, blank=True, null=True)

    # Landlord contact info
    landlord_cell  = models.CharField(max_length=50, blank=True, null=True)
    landlord_email = models.EmailField(blank=True, null=True)

    # Availability toggle
    is_available = models.BooleanField(default=True)  # True=Available, False=Occupied

    # Primary fields
    bedrooms  = models.IntegerField(default=1)
    bathrooms = models.IntegerField(default=1)

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPES,
        default='house'
    )

    pets_allowed          = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    ada_accessible        = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    income_requirement    = models.CharField(max_length=20, choices=INCOME_CHOICES, blank=True, null=True)
    past_eviction_allowed = models.BooleanField(choices=YES_NO_CHOICES, default=False)
    sex_offender_allowed  = models.BooleanField(choices=YES_NO_CHOICES, default=False)

    # Now a choice field (none, misdemeanor, felony)
    criminal_record_allowed = models.CharField(
        max_length=12,
        choices=CRIMINAL_RECORD_CHOICES,
        default='none'
    )

    # Keep the original additional_info
    additional_info = models.TextField(blank=True, null=True)

    # NEW: replace "issues_allowed" (bool) with "misc_notes" (text)
    misc_notes = models.TextField(blank=True, null=True)

    # Multiple images
    image1 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='property_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='property_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.street or ''} {self.city or ''}, {self.state or ''} {self.zip or ''}"
