from django.urls import path
from . import views

app_name = "housing_app"

urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("export/csv/", views.export_listings_csv, name="export_csv"),
    path("export/pdf/", views.export_listings_pdf, name="export_pdf"),
    path("listing/<int:pk>/", views.listing_detail, name="listing_detail"),
    path("listing/create/", views.listing_create, name="listing_create"),
    path("listing/<int:pk>/update/", views.listing_update, name="listing_update"),
    path("listing/<int:pk>/delete/", views.listing_delete, name="listing_delete"),
    path("scrape/", views.scrape_listings_view, name="scrape_listings"),
    path("scrape/api/", views.scrape_api_view, name="scrape_api"),
    path("register/", views.register, name="register"),
]
