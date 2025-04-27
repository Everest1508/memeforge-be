from django.contrib import admin
from django.utils.html import format_html
from .models import UserSubmission

@admin.register(UserSubmission)
class UserSubmissionAdmin(admin.ModelAdmin):
    list_display = ('email', 'vercel_blob_url', 'x_post_url', 'created_at', 'image_preview')
    search_fields = ('email', 'vercel_blob_url', 'x_post_url')
    list_filter = ('created_at',)

    # Add image preview function
    def image_preview(self, obj):
        if obj.vercel_blob_url:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.vercel_blob_url)
        return "No image available"
    
    image_preview.short_description = "Image Preview"
