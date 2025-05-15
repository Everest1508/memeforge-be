# serializers.py

from rest_framework import serializers
from .models import MemeforgeUser

class MemeforgeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemeforgeUser
        fields = ['email', 'profile_picture', 'twitter_x_account']
