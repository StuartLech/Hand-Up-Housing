from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'street',
            'city',
            'state',
            'zip',
            'landlord_cell',
            'landlord_email',
            'is_available',
            'bedrooms',
            'bathrooms',
            'property_type',
            'pets_allowed',
            'ada_accessible',
            'income_requirement',
            'past_eviction_allowed',
            'sex_offender_allowed',
            'criminal_record_allowed',
            'additional_info',   # Kept as is
            'misc_notes',        # Replaces issues_allowed
            'image1',
            'image2',
            'image3',
        ]
