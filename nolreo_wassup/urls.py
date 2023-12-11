from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('lodging/', include('lodging.urls')),
    path('traffic/', include('traffic.urls')),
    path('pick/', include('pick.urls')),
    path('reservation/', include('reservation.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)