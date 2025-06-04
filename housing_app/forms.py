from django import forms
from django.forms import inlineformset_factory
from .models import Listing, ListingImage


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "street",
            "city",
            "state",
            "zip",
            "landlord_cell",
            "landlord_email",
            "is_available",
            "bedrooms",
            "bathrooms",
            "property_type",
            "pets_allowed",
            "ada_accessible",
            "income_requirement",
            "past_eviction_allowed",
            "sex_offender_allowed",
            "criminal_record_allowed",
            "additional_info",  # Kept as is
            "misc_notes",  # Replaces issues_allowed
        ]


# Up to 50 images per listing
ListingImageFormSet = inlineformset_factory(
    Listing,
    ListingImage,
    fields=["image"],
    extra=1,
    can_delete=True,
    max_num=50,
)


# Simple form to trigger scraping from one or more URLs
class ScrapeURLForm(forms.Form):
    urls = forms.CharField(
        label="Listing URLs",
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Enter one URL per line",
    )


# Form for scraping from an external API endpoint
class ScrapeAPIForm(forms.Form):
    api_url = forms.URLField(label="API Endpoint")
    api_key = forms.CharField(label="API Key", required=False)


class TwoFactorCodeForm(forms.Form):
    code = forms.CharField(label="Authentication Code", max_length=6)
