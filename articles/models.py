from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from categories.models import Category, Tag
from publications.models import Publication

class Article(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="articles")
    tags = models.ManyToManyField(Tag, blank=True, related_name="articles")
    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="articles",
        null=True,
        blank=True
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    content = models.TextField()
    cover_image = models.ImageField(upload_to="articles/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=300, blank=True)
    reading_time = models.PositiveIntegerField(default=1)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "article"
            slug = base
            counter = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f"{base}-{counter}"
            self.slug = slug
        words = len(self.content.split())
        self.reading_time = max(1, round(words / 200))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title