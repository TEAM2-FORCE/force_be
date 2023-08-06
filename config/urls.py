from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('products/', include('products.urls')),

    path('ingredients/', include('ingredints.urls')),
]
