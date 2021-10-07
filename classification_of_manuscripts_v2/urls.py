from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from classification_of_manuscripts_v2 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('backend.api.v1.urls')),
    path('about/', include('frontend.about.urls'), name='about'),
    path('', include('frontend.index.urls'), name='index'),
    path('manuscript/', include('frontend.manuscript.urls'), name='index'),
]

# пока сервер на локальной машине
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

