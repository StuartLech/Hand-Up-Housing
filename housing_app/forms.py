from django import forms
from django.forms import inlineformset_factory
from .models import Listing, ListingImage

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
        ]

# Up to 50 images per listing
ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    fields=['image'],
    extra=1,
    can_delete=True,
    max_num=50,
)


class ScrapeURLForm(forms.Form):
    """Accept one or more URLs to scrape."""
    urls = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter one URL per line",
        label="Listing URLs",
    )

    def clean_urls(self):
        raw = self.cleaned_data.get("urls", "")
        lines = [line.strip() for line in raw.splitlines() if line.strip()]
        validator = forms.URLField().clean
        cleaned = []
        for line in lines:
            cleaned.append(validator(line))
        return cleaned
