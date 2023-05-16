"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Madrasha API",
        default_version='v1',
        description="Test description",
        terms_of_service="madrashabd.com",
        contact=openapi.Contact(email="info@ikhwanbd.com"),
        license=openapi.License(name="Ikhwan Bangaldesh"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

from django.urls import path


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settingapp.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('transactions/', include('transactions.urls')),
    path('library/', include('library.urls')),
    path('boarding/', include('boarding.urls')),
    path('committee/', include('committees.urls')),
    path('talimat/', include('talimats.urls')),
    path('transport/', include('transport.urls')),
    path('darul-ekama/', include('darul_ekama.urls')),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('glitchtip-debug/', trigger_error),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
