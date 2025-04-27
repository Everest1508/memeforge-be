from rest_framework import serializers
from .models import UserSubmission

class UserSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubmission
        fields = ['vercel_blob_url', 'email', 'created_at']
        read_only_fields = ['created_at']  # Prevent clients from modifying 'created_at'
