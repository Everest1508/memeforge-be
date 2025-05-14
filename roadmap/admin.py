from django.contrib import admin
from .models import Roadmap, RoadmapImage

class RoadmapImageInline(admin.TabularInline):
    model = RoadmapImage
    extra = 1

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RoadmapImageInline]
