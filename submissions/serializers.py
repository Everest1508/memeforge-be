from rest_framework import serializers
from .models import UserSubmission

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = ['id', 'vercel_blob_url', 'email', 'x_post_url', 'created_at']
