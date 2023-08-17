from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/', include('allauth.urls')),

    path('products/', include('products.urls')),

    path('ingredients/', include('ingredients.urls')),
]

# nginx(웹서버) 정적파일 로딩
from django.conf.urls.static import static
from django.conf import settings
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
