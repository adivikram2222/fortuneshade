"""
URL configuration for fortune project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # App URLs
    path('', include('app.urls', namespace='app')),
    
    # Favicon
    path('favicon.ico', TemplateView.as_view(template_name='favicon.ico', content_type='image/x-icon')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Error handlers
handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
