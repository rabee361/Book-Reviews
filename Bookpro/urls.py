
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('bookapp.urls')),
    path('api/' , include('bookapp.api.urls')),
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)