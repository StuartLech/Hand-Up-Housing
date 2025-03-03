from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q

from .models import Listing
from .forms import ListingForm

def is_volunteer(user):
    return user.groups.filter(name='Volunteer').exists() or user.is_superuser

def is_social_worker(user):
    return user.groups.filter(name='Social Worker').exists() or user.is_superuser

def is_admin(user):
    return user.is_superuser

def is_approved(user):
    return (
        user.groups.filter(name='Volunteer').exists()
        or user.groups.filter(name='Social Worker').exists()
        or user.is_superuser
    )

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
    email = forms.EmailField(required=True, help_text="Enter a valid email address")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name  = self.cleaned_data["last_name"]
        user.email      = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
@user_passes_test(is_approved)
def listing_list(request):
    """ Show all available listings by default; can show occupied if user requests. """
    qs = Listing.objects.all()

    # If not set to "show_occupied=1", we filter out is_available=False (occupied)
    show_occupied = request.GET.get('show_occupied', '0')
    if show_occupied != '1':
        qs = qs.filter(is_available=True)

    # 1) Search bar (search across address fields, landlord info, additional_info, misc_notes)
    search = request.GET.get('search')
    if search:
        qs = qs.filter(
            Q(street__icontains=search)  |
            Q(city__icontains=search)    |
            Q(state__icontains=search)   |
            Q(zip__icontains=search)     |
            Q(landlord_cell__icontains=search) |
            Q(landlord_email__icontains=search) |
            Q(additional_info__icontains=search) |
            Q(misc_notes__icontains=search)
        )

    # 2) Filter: bedrooms (min)
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        qs = qs.filter(bedrooms__gte=bedrooms)

    # 3) Filter: bathrooms (min)
    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        qs = qs.filter(bathrooms__gte=bathrooms)

    # 4) property_type
    property_type = request.GET.get('property_type')
    if property_type:
        qs = qs.filter(property_type=property_type)

    # 5) pets_allowed
    pets_allowed = request.GET.get('pets_allowed')
    if pets_allowed in ['True', 'False']:
        qs = qs.filter(pets_allowed=(pets_allowed == 'True'))

    # 6) ada_accessible
    ada_accessible = request.GET.get('ada_accessible')
    if ada_accessible in ['True', 'False']:
        qs = qs.filter(ada_accessible=(ada_accessible == 'True'))

    # 7) past_eviction_allowed
    past_eviction_allowed = request.GET.get('past_eviction_allowed')
    if past_eviction_allowed in ['True', 'False']:
        qs = qs.filter(past_eviction_allowed=(past_eviction_allowed == 'True'))

    # 8) sex_offender_allowed
    sex_offender_allowed = request.GET.get('sex_offender_allowed')
    if sex_offender_allowed in ['True', 'False']:
        qs = qs.filter(sex_offender_allowed=(sex_offender_allowed == 'True'))

    # 9) criminal_record_allowed
    criminal_record_allowed = request.GET.get('criminal_record_allowed')
    if criminal_record_allowed in ['none', 'misdemeanor', 'felony']:
        qs = qs.filter(criminal_record_allowed=criminal_record_allowed)

    # 10) income_requirement
    inc_req = request.GET.get('income_requirement')
    if inc_req in ['under_20', '30_40', '40_50', '50_plus']:
        qs = qs.filter(income_requirement=inc_req)

    return render(request, 'housing_app/listing_list.html', {'listings': qs})

@login_required
@user_passes_test(is_approved)
def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'housing_app/listing_detail.html', {'listing': listing})

@login_required
@user_passes_test(is_volunteer)
def listing_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('housing_app:listing_list')
    else:
        form = ListingForm()
    return render(request, 'housing_app/listing_create.html', {'form': form})

@login_required
@user_passes_test(is_volunteer)
def listing_update(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('housing_app:listing_detail', pk=pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'housing_app/listing_update.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        listing.delete()
        return redirect('housing_app:listing_list')
    return render(request, 'housing_app/listing_detail.html', {'listing': listing})
