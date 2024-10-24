from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_ts
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("api.router")),
    # path("apps/", include("apps.individual_schedule.urls")),
    path('apps/', include('apps.o_task.urls')),
]


urlpatterns += doc_ts

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
