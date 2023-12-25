from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, 
                                    SpectacularSwaggerView, SpectacularJSONAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('lodging/', include('lodging.urls')),
    path('traffic/', include('traffic.urls')),
    path('pick/', include('pick.urls')),
    path('reservation/', include('reservation.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='schema-json'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)