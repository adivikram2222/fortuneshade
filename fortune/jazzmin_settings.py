# Jazzmin settings
JAZZMIN_SETTINGS = {
    # title of the window
    "site_title": "FortuneShade Admin",
    
    # Title on the login screen
    "site_header": "FortuneShade",
    
    # Title on the brand
    "site_brand": "FortuneShade",
    
    # Logo to use for your site
    "site_logo": "images/logo.png",
    
    # CSS classes that are applied to the logo
    "site_logo_classes": "img-circle",
    
    # Welcome text on the login screen
    "welcome_sign": "Welcome to FortuneShade Admin",
    
    # Copyright on the footer
    "copyright": "FortuneShade Ltd",
    
    # The model admin to search from the search bar
    "search_model": "auth.User",
    
    # Top menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
        {"model": "auth.User"},
    ],
    
    # User menu
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "app.SiteSetting", "app.HeroSection", "app.Feature", "app.Statistic", "app.Testimonial"],
    
    # Icons for side menu apps/models
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "app.SiteSetting": "fas fa-cogs",
        "app.HeroSection": "fas fa-home",
        "app.Feature": "fas fa-star",
        "app.Statistic": "fas fa-chart-bar",
        "app.Testimonial": "fas fa-quote-right",
        "app.PricingPlan": "fas fa-dollar-sign",
        "app.FAQ": "fas fa-question-circle",
        "app.BlogCategory": "fas fa-folder",
        "app.BlogPost": "fas fa-newspaper",
    },
    
    # Default icons
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related Modal
    "related_modal_active": True,
    
    # UI Tweaks
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": True,
    
    # Change view
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
        "app.SiteSetting": "vertical_tabs",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
