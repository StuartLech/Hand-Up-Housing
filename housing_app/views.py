from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import Q, IntegerField  # ADDED IntegerField import
from django.db.models.functions import Cast   # ADDED Cast import

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
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
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
    qs = Listing.objects.all()

    # 1) Search bar: substring across address, landlord_contact, additional_info
    search = request.GET.get('search')
    if search:
        qs = qs.filter(
            Q(address__icontains=search) |
            Q(landlord_contact__icontains=search) |
            Q(additional_info__icontains=search)
        )

    # 2) Filter: bedrooms (min)
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        qs = qs.filter(bedrooms__gte=bedrooms)

    # 3) Filter: bathrooms (min)
    bathrooms = request.GET.get('bathrooms')
    if bathrooms:
        qs = qs.filter(bathrooms__gte=bathrooms)

    # 4) Filter: property_type
    property_type = request.GET.get('property_type')
    if property_type:
        qs = qs.filter(property_type=property_type)

    # 5) Filter: pets_allowed
    pets_allowed = request.GET.get('pets_allowed')
    if pets_allowed in ['True', 'False']:
        qs = qs.filter(pets_allowed=(pets_allowed == 'True'))

    # 6) Filter: ada_accessible
    ada_accessible = request.GET.get('ada_accessible')
    if ada_accessible in ['True', 'False']:
        qs = qs.filter(ada_accessible=(ada_accessible == 'True'))

    # 7) Filter: past_eviction_allowed
    past_eviction_allowed = request.GET.get('past_eviction_allowed')
    if past_eviction_allowed in ['True', 'False']:
        qs = qs.filter(past_eviction_allowed=(past_eviction_allowed == 'True'))

    # 8) Filter: sex_offender_allowed
    sex_offender_allowed = request.GET.get('sex_offender_allowed')
    if sex_offender_allowed in ['True', 'False']:
        qs = qs.filter(sex_offender_allowed=(sex_offender_allowed == 'True'))

    # 9) Filter: criminal_record_allowed
    criminal_record_allowed = request.GET.get('criminal_record_allowed')
    if criminal_record_allowed in ['True', 'False']:
        qs = qs.filter(criminal_record_allowed=(criminal_record_allowed == 'True'))

    # 10) Filter: issues_allowed
    issues_allowed = request.GET.get('issues_allowed')
    if issues_allowed in ['True', 'False']:
        qs = qs.filter(issues_allowed=(issues_allowed == 'True'))

    # 11) Filter: income_requirement -> less than or equal to user input (if numeric)
    inc_req = request.GET.get('income_requirement')
    if inc_req:
        try:
            salary = int(inc_req)
            # Cast the CharField to integer, then do LTE filter
            qs = qs.annotate(
                inc_int=Cast('income_requirement', IntegerField())
            ).filter(inc_int__lte=salary)
        except ValueError:
            # If not numeric, do nothing (or we could fallback to substring match)
            pass

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
        form = ListingForm(request.POST, request.FILES)  # request.FILES if images
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

