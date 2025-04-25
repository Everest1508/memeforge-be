from django.db import models

class ImageCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Image Categories"

    def __str__(self):
        return self.name


class Image(models.Model):
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=200)
    short_description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='team/')
    x_account = models.URLField("X (Twitter) Profile", blank=True)
    short_description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Template(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='templates/')
    short_description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
