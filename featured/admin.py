from django.contrib import admin
from .models import Featured, TabiPayCard, QuestionCategory, MCQQuestion, MCQOption

@admin.register(Featured)
class FeaturedAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']

@admin.register(TabiPayCard)
class TabiPayCardAdmin(admin.ModelAdmin):
    list_display = ['title']

class MCQOptionInline(admin.TabularInline):
    model = MCQOption
    extra = 2

@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category']
    inlines = [MCQOptionInline]

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
