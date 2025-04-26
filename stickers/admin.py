from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Image, ImageCategory, TeamMember, Template
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html



@admin.register(ImageCategory)
class ImageCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'image_preview')
    list_filter = ('category',)
    search_fields = ('title', 'short_description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 300px;" />', obj.image.url)
        return "No image available"
    
    image_preview.short_description = "Image Preview"

@admin.register(TeamMember)
class TeamMemberAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ('name', 'x_account')
    summernote_fields = ('short_description',)



@admin.register(Template)
class TemplateAdmin(ImportExportModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name', 'short_description')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 300px;" />', obj.image.url)
        return "No image available"
    
    image_preview.short_description = "Image Preview"