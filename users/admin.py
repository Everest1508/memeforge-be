from django.contrib import admin
from django.utils.html import format_html
from .models import MemeforgeUser, UserTabiPayCardOverlay
from django.db.models import Count

@admin.register(MemeforgeUser)
class MemeforgeUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'x_account', 'submission_count', 'profile_picture_preview')
    readonly_fields = ('profile_picture_preview',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(sub_count=Count('submissions'))

    def submission_count(self, obj):
        from submissions.models import UserSubmission
        return UserSubmission.objects.filter(email=obj.email).count()
    submission_count.short_description = 'Submissions'

    def profile_picture_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture)
        return "-"
    profile_picture_preview.short_description = 'Profile Pic'


@admin.register(UserTabiPayCardOverlay)
class UserTabiPayCardAdmin(admin.ModelAdmin):
    list_display =['id','username_text', 'name_text']
    pass