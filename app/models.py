from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    primary_cta_text = models.CharField(max_length=100)
    primary_cta_link = models.CharField(max_length=200)
    secondary_cta_text = models.CharField(max_length=100, blank=True)
    secondary_cta_link = models.CharField(max_length=200, blank=True)
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"


class Statistic(models.Model):
    value = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.label}: {self.value}"

    class Meta:
        ordering = ['order']


class Feature(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon_class = models.CharField(max_length=50, help_text="Font Awesome icon class")
    icon_bg_color = models.CharField(max_length=50, default="bg-blue-100")
    icon_text_color = models.CharField(max_length=50, default="text-blue-600")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.role}"


class PricingPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual')
    ])
    description = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.get_billing_cycle_display()})"

    class Meta:
        ordering = ['order']


class PlanFeature(models.Model):
    plan = models.ForeignKey(PricingPlan, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.plan.name} - {self.text[:50]}"

    class Meta:
        ordering = ['order']


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class SiteSetting(models.Model):
    # Basic Site Information
    site_name = models.CharField(max_length=100, default="FortuneShade")
    site_name_suffix = models.CharField(max_length=100, blank=True, help_text="Optional suffix for the site name that will be styled differently")
    site_description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(default="support@fortuneshade.com")
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # About Section
    about_text = models.TextField(blank=True, help_text="Text for the about section")
    about_image = models.ImageField(upload_to='site/', blank=True, null=True)
    mission_text = models.TextField(blank=True, help_text="Mission statement text")
    founder_name = models.CharField(max_length=100, blank=True)
    quote_text = models.TextField(blank=True, help_text="Quote text for the about section")
    years_experience = models.CharField(max_length=50, blank=True, help_text="Years of experience to display")
    students_count = models.CharField(max_length=50, blank=True, help_text="Number of students/members to display")
    
    # Footer Settings
    footer_tagline = models.TextField(blank=True, help_text="Tagline to display in the footer")
    newsletter_text = models.TextField(blank=True, help_text="Text for the newsletter signup section")
    privacy_url = models.URLField(blank=True, help_text="URL to the privacy policy page")
    terms_url = models.URLField(blank=True, help_text="URL to the terms of service page")
    cookie_url = models.URLField(blank=True, help_text="URL to the cookie policy page")
    copyright_text = models.CharField(max_length=255, default="© 2025 FortuneShade. All rights reserved.")
    
    # CTA Section
    cta_title = models.CharField(max_length=200, blank=True, help_text="Title for the CTA section")
    cta_text = models.TextField(blank=True, help_text="Text for the CTA section")
    cta_button_text = models.CharField(max_length=100, blank=True, help_text="Text for the CTA button")
    cta_image = models.ImageField(upload_to='site/', blank=True, null=True, help_text="Image for the CTA section")
    guarantee_icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class for the guarantee icon")
    guarantee_title = models.CharField(max_length=100, blank=True, help_text="Title for the guarantee badge")
    guarantee_text = models.CharField(max_length=200, blank=True, help_text="Text for the guarantee badge")
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = RichTextField()
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    excerpt = models.TextField(max_length=300, blank=True, help_text="Short description displayed in blog listings")
    content = RichTextField()
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
