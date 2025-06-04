# housing_site/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from housing_app.views import TwoFactorLoginView, two_factor_verify, enable_two_factor

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', TwoFactorLoginView.as_view(), name='login'),
    path('accounts/2fa/', two_factor_verify, name='two_factor_verify'),
    path('accounts/setup-2fa/', enable_two_factor, name='enable_two_factor'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('housing_app.urls', namespace='housing_app')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
