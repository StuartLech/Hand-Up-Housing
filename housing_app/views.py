from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q
from django.urls import reverse
import pyotp

from .models import Listing, ActivityLog, UserProfile, Favorite
from .forms import (
    ListingForm,
    ListingImageFormSet,
    ScrapeURLForm,
    ScrapeAPIForm,
    TwoFactorCodeForm,
)
from .scraper import scrape_urls, scrape_api


def is_manager(user):
    return user.groups.filter(name="Manager").exists() or user.is_superuser


def is_client_services(user):
    return user.groups.filter(name="Client Services").exists() or user.is_superuser


def is_admin(user):
    return user.is_superuser


def is_approved(user):
    return (
        user.groups.filter(name="Manager").exists()
        or user.groups.filter(name="Client Services").exists()
        or user.is_superuser
    )


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class TwoFactorLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        user = form.get_user()
        profile = getattr(user, "userprofile", None)
        if profile and profile.two_factor_secret:
            self.request.session["pre_2fa_user_id"] = user.id
            return redirect("two_factor_verify")
        return super().form_valid(form)


def two_factor_verify(request):
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(id=user_id)
    profile = user.userprofile
    if request.method == "POST":
        form = TwoFactorCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            totp = pyotp.TOTP(profile.two_factor_secret)
            if totp.verify(code):
                login(request, user)
                request.session.pop("pre_2fa_user_id", None)
                return redirect("housing_app:listing_list")
            else:
                form.add_error("code", "Invalid code")
    else:
        form = TwoFactorCodeForm()
    return render(request, "registration/two_factor_verify.html", {"form": form})


@login_required
def enable_two_factor(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        secret = request.session.get("temp_2fa_secret")
        if not secret:
            return redirect("enable_two_factor")
        form = TwoFactorCodeForm(request.POST)
        if form.is_valid():
            totp = pyotp.TOTP(secret)
            if totp.verify(form.cleaned_data["code"]):
                profile.two_factor_secret = secret
                profile.save()
                request.session.pop("temp_2fa_secret", None)
                return redirect("housing_app:listing_list")
            else:
                form.add_error("code", "Invalid code")
    else:
        secret = request.session.get("temp_2fa_secret")
        if not secret:
            secret = pyotp.random_base32()
            request.session["temp_2fa_secret"] = secret
        form = TwoFactorCodeForm()

    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        request.user.username, issuer_name="HUH Connect"
    )
    return render(
        request,
        "housing_app/enable_two_factor.html",
        {"secret": secret, "uri": totp_uri, "form": form},
    )


@login_required
@user_passes_test(is_approved)
def listing_list(request):
    """Show all available listings by default; can show occupied if user requests."""
    qs = Listing.objects.all()

    # If not set to "show_occupied=1", we filter out is_available=False (occupied)
    show_occupied = request.GET.get("show_occupied", "0")
    if show_occupied != "1":
        qs = qs.filter(is_available=True)

    # 1) Search bar (search across address fields, landlord info, additional_info, misc_notes)
    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(street__icontains=search)
            | Q(city__icontains=search)
            | Q(state__icontains=search)
            | Q(zip__icontains=search)
            | Q(landlord_cell__icontains=search)
            | Q(landlord_email__icontains=search)
            | Q(additional_info__icontains=search)
            | Q(misc_notes__icontains=search)
        )

    # 2) Filter: bedrooms (min)
    bedrooms = request.GET.get("bedrooms")
    if bedrooms:
        qs = qs.filter(bedrooms__gte=bedrooms)

    # 3) Filter: bathrooms (min)
    bathrooms = request.GET.get("bathrooms")
    if bathrooms:
        qs = qs.filter(bathrooms__gte=bathrooms)

    # 4) property_type
    property_type = request.GET.get("property_type")
    if property_type:
        qs = qs.filter(property_type=property_type)

    # 5) pets_allowed
    pets_allowed = request.GET.get("pets_allowed")
    if pets_allowed in ["True", "False"]:
        qs = qs.filter(pets_allowed=(pets_allowed == "True"))

    # 6) ada_accessible
    ada_accessible = request.GET.get("ada_accessible")
    if ada_accessible in ["True", "False"]:
        qs = qs.filter(ada_accessible=(ada_accessible == "True"))

    # 7) past_eviction_allowed
    past_eviction_allowed = request.GET.get("past_eviction_allowed")
    if past_eviction_allowed in ["True", "False"]:
        qs = qs.filter(past_eviction_allowed=(past_eviction_allowed == "True"))

    # 8) sex_offender_allowed
    sex_offender_allowed = request.GET.get("sex_offender_allowed")
    if sex_offender_allowed in ["True", "False"]:
        qs = qs.filter(sex_offender_allowed=(sex_offender_allowed == "True"))

    # 9) criminal_record_allowed
    criminal_record_allowed = request.GET.get("criminal_record_allowed")
    if criminal_record_allowed in ["none", "misdemeanor", "felony"]:
        qs = qs.filter(criminal_record_allowed=criminal_record_allowed)

    # 10) income_requirement
    inc_req = request.GET.get("income_requirement")
    if inc_req in ["under_20", "30_40", "40_50", "50_plus"]:
        qs = qs.filter(income_requirement=inc_req)

    return render(request, "housing_app/listing_list.html", {"listings": qs})


@login_required
@user_passes_test(is_approved)
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, listing=listing
        ).exists()
    return render(
        request,
        "housing_app/listing_detail.html",
        {"listing": listing, "is_favorite": is_favorite},
    )


@login_required
@user_passes_test(is_manager)
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        formset = ListingImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            listing = form.save()
            formset.instance = listing
            formset.save()
            ActivityLog.objects.create(
                user=request.user, action="created listing", listing=listing
            )
            return redirect("housing_app:listing_list")
    else:
        form = ListingForm()
        formset = ListingImageFormSet()
    return render(
        request, "housing_app/listing_create.html", {"form": form, "formset": formset}
    )


@login_required
@user_passes_test(is_manager)
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        formset = ListingImageFormSet(request.POST, request.FILES, instance=listing)
        if form.is_valid() and formset.is_valid():
            listing = form.save()
            formset.instance = listing
            formset.save()
            ActivityLog.objects.create(
                user=request.user, action="updated listing", listing=listing
            )
            return redirect("housing_app:listing_detail", pk=pk)
    else:
        form = ListingForm(instance=listing)
        formset = ListingImageFormSet(instance=listing)
    return render(
        request, "housing_app/listing_update.html", {"form": form, "formset": formset}
    )


@login_required
@user_passes_test(is_admin)
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == "POST":
        ActivityLog.objects.create(
            user=request.user, action="deleted listing", listing=listing
        )
        listing.delete()
        return redirect("housing_app:listing_list")
    return render(request, "housing_app/listing_detail.html", {"listing": listing})


@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        fav.delete()
    return redirect(
        request.META.get(
            "HTTP_REFERER", reverse("housing_app:listing_detail", args=[pk])
        )
    )


@login_required
def favorite_list(request):
    listings = Listing.objects.filter(favorites__user=request.user)
    return render(request, "housing_app/favorite_list.html", {"listings": listings})


@login_required
@user_passes_test(is_manager)
def scrape_listings_view(request):
    """Allow managers to scrape listings by providing URLs."""
    results = None
    if request.method == "POST":
        form = ScrapeURLForm(request.POST)
        if form.is_valid():
            urls = [
                u.strip() for u in form.cleaned_data["urls"].splitlines() if u.strip()
            ]
            results = scrape_urls(urls)
            ActivityLog.objects.create(user=request.user, action="scraped listings")
    else:
        form = ScrapeURLForm()
    return render(
        request,
        "housing_app/scrape_listings.html",
        {
            "form": form,
            "results": results,
        },
    )


@login_required
@user_passes_test(is_manager)
def scrape_api_view(request):
    """Allow managers to import listings from an API endpoint."""
    results = None
    if request.method == "POST":
        form = ScrapeAPIForm(request.POST)
        if form.is_valid():
            api_url = form.cleaned_data["api_url"]
            api_key = form.cleaned_data.get("api_key")
            results = scrape_api(api_url, api_key)
            ActivityLog.objects.create(user=request.user, action="imported listings")
    else:
        form = ScrapeAPIForm()
    return render(
        request,
        "housing_app/scrape_api.html",
        {
            "form": form,
            "results": results,
        },
    )
