from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import (
    HeroSection, Statistic, Feature, Testimonial,
    PricingPlan, FAQ, SiteSetting, Page, BlogCategory, BlogPost
)
import random


def get_site_settings():
    """Helper function to get or create site settings"""
    settings_obj = cache.get('site_settings')
    if not settings_obj:
        settings_obj = SiteSetting.objects.first()
        if not settings_obj:
            # Create default settings if none exist
            settings_obj = SiteSetting.objects.create()
        cache.set('site_settings', settings_obj, 3600)  # Cache for 1 hour
    return settings_obj


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get or create site settings
        site_settings = get_site_settings()
        context['site_settings'] = site_settings
        
        # Get active hero section
        context['hero'] = HeroSection.objects.filter(is_active=True).first()
        
        # Get active statistics
        context['statistics'] = Statistic.objects.filter(is_active=True).order_by('order')[:4]
        
        # Get active features
        context['features'] = Feature.objects.filter(is_active=True).order_by('order')[:9]
        
        # Get featured testimonials
        context['testimonials'] = Testimonial.objects.filter(
            is_active=True, 
            is_featured=True
        ).order_by('-created_at')[:6]
        
        # Get pricing plans with features
        context['pricing_plans'] = PricingPlan.objects.filter(
            is_active=True
        ).prefetch_related('features').order_by('order')
        
        # Get active FAQs
        context['faqs'] = FAQ.objects.filter(is_active=True).order_by('order')
        
        # Add about section image from site settings if available
        if site_settings.about_image:
            context['about_image'] = site_settings.about_image.url
        
        # Create dummy process steps (in a real application, this would be from a model)
        context['process_steps'] = [
            {
                'title': 'Learn The System',
                'description': 'Begin by mastering our proven trading strategy through our comprehensive course material and video tutorials.',
                'icon_url': '/api/placeholder/80/80'
            },
            {
                'title': 'Watch & Practice',
                'description': 'Join our daily live trading sessions to see the strategy in action and practice with our paper trading simulator.',
                'icon_url': '/api/placeholder/80/80'
            },
            {
                'title': 'Trade & Grow',
                'description': 'Start trading real capital with the support of our community and mentors, gradually scaling your account as you gain consistency.',
                'icon_url': '/api/placeholder/80/80'
            }
        ]
        
        # Create dummy CTA benefits (in a real application, this would be from a model)
        context['cta_benefits'] = [
            {
                'icon_class': 'fas fa-user-tie',
                'text': 'Expert Mentorship'
            },
            {
                'icon_class': 'fas fa-video',
                'text': 'Live Trading Sessions'
            },
            {
                'icon_class': 'fas fa-chart-line',
                'text': 'Proven Trading System'
            },
            {
                'icon_class': 'fas fa-users',
                'text': 'Supportive Community'
            }
        ]
        
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = 'page.html'
    context_object_name = 'page'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Page.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        context['featured_posts'] = BlogPost.objects.filter(is_active=True, is_featured=True).order_by('-published_at')[:3]
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        return context


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    
    def get_queryset(self):
        return BlogPost.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        
        # Get related posts from the same category
        post = self.get_object()
        related_posts = BlogPost.objects.filter(
            category=post.category, 
            is_active=True
        ).exclude(id=post.id).order_by('-published_at')[:3]
        
        context['related_posts'] = related_posts
        return context


class BlogCategoryView(ListView):
    template_name = 'blog_category.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(BlogCategory, slug=self.kwargs['slug'], is_active=True)
        return BlogPost.objects.filter(category=self.category, is_active=True).order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = get_site_settings()
        context['category'] = self.category
        context['categories'] = BlogCategory.objects.filter(is_active=True)
        return context
