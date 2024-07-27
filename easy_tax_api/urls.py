from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


url_v1 = [
    path('', include('users.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dev/', include(url_v1))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
