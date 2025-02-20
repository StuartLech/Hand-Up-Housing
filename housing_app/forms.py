# housing_app/forms.py

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'address',
            'landlord_contact',
            'bedrooms',
            'bathrooms',
            'property_type',
            'pets_allowed',
            'ada_accessible',
            'income_requirement',
            'past_eviction_allowed',
            'sex_offender_allowed',
            'criminal_record_allowed',
            'issues_allowed',
            'additional_info',
            'image',
        ]
