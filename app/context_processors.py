from django.core.cache import cache
from .models import SiteSetting

def site_settings(request):
    """Makes site settings available in all templates."""
    settings_obj = cache.get('site_settings')
    if not settings_obj:
        settings_obj = SiteSetting.objects.first()
        if not settings_obj:
            # Create default settings if none exist
            settings_obj = SiteSetting.objects.create()
        cache.set('site_settings', settings_obj, 3600)  # Cache for 1 hour
    return {'site_settings': settings_obj}
