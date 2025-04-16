from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Image, ImageCategory, TeamMember
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ImageCategory)
class ImageCategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    list_display = ('title', 'category', 'uploaded_at')
    list_filter = ('category',)
    search_fields = ('title', 'short_description')

@admin.register(TeamMember)
class TeamMemberAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    list_display = ('name', 'x_account')
    summernote_fields = ('short_description',)
