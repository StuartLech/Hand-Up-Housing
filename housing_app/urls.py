# housing_app/urls.py
from django.urls import path
from . import views

app_name = 'housing_app'

urlpatterns = [
    path('', views.listing_list, name='listing_list'),
    path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('listing/create/', views.listing_create, name='listing_create'),
    path('listing/<int:pk>/update/', views.listing_update, name='listing_update'),
    path('listing/<int:pk>/delete/', views.listing_delete, name='listing_delete'),
    path('register/', views.register, name='register'),
]
