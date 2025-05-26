from django.contrib import admin
from .models import (
    HeroSection, Statistic, Feature, Testimonial, 
    PricingPlan, PlanFeature, FAQ, SiteSetting, Page,
    BlogCategory, BlogPost
)
from django.utils.html import format_html


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'subtitle')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'subtitle')
        }),
        ('Call to Action', {
            'fields': (
                'primary_cta_text', 'primary_cta_link',
                'secondary_cta_text', 'secondary_cta_link'
            )
        }),
        ('Media', {
            'fields': ('background_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'icon_class', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('label', 'value')


class PlanFeatureInline(admin.TabularInline):
    model = PlanFeature
    extra = 1
    fields = ('text', 'is_available', 'order')
    ordering = ('order',)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'billing_cycle', 'is_featured', 'is_active', 'order')
    list_editable = ('price', 'billing_cycle', 'is_featured', 'is_active', 'order')
    list_filter = ('is_featured', 'is_active', 'billing_cycle')
    search_fields = ('name', 'description')
    inlines = [PlanFeatureInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'billing_cycle', 'description')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class', 'order', 'is_active')
    list_editable = ('icon_class', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Styling', {
            'fields': ('icon_class', 'icon_bg_color', 'icon_text_color')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'company', 'rating', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'rating', 'created_at')
    search_fields = ('name', 'role', 'company', 'content')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Testimonial Details', {
            'fields': ('name', 'role', 'company', 'content', 'rating')
        }),
        ('Media', {
            'fields': ('avatar',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('question', 'answer')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'category')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only one instance is allowed
        return not SiteSetting.objects.exists()
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No logo"
    
    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" style="max-height: 32px;" />', obj.favicon.url)
        return "No favicon"
    
    logo_preview.short_description = 'Logo Preview'
    favicon_preview.short_description = 'Favicon Preview'
    
    list_display = ('site_name', 'contact_email', 'updated_at')
    readonly_fields = ('updated_at', 'logo_preview', 'favicon_preview')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'site_description', 'contact_email', 'phone_number', 'address')
        }),
        ('Media', {
            'fields': ('logo', 'logo_preview', 'favicon', 'favicon_preview')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
            'classes': ('collapse',)
        }),
        ('Footer', {
            'fields': ('copyright_text',)
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Page Content', {
            'fields': ('title', 'slug', 'content')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active', 'published_at')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at', 'published_at')
    search_fields = ('title', 'content', 'excerpt', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_at'
    fieldsets = (
        ('Post Content', {
            'fields': ('title', 'slug', 'category', 'excerpt', 'content')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
