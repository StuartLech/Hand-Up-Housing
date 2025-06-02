# housing_app/admin.py

from django.contrib import admin
from .models import Listing, ListingImage, UserProfile, ActivityLog


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingImageInline]


admin.site.register(ListingImage)
admin.site.register(UserProfile)
admin.site.register(ActivityLog)
