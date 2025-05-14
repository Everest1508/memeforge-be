from django.db import models
from django.utils.text import slugify

class Roadmap(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0, help_text="Used for sorting roadmap steps")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class RoadmapImage(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='roadmap/')
    caption = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.roadmap.title}"
