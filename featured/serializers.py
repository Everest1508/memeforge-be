# serializers.py
from rest_framework import serializers
from .models import Featured, TabiPayCard, QuestionCategory, MCQQuestion, MCQOption

class FeaturedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Featured
        fields = ['id', 'title', 'description', 'image', 'url', 'is_coming_soon']

class TabiPayCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabiPayCard
        fields = ['id', 'title', 'image', 'description']

class MCQOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQOption
        fields = ['id', 'option_text']

class MCQQuestionSerializer(serializers.ModelSerializer):
    options = MCQOptionSerializer(many=True)

    class Meta:
        model = MCQQuestion
        fields = ['id', 'question_text', 'options']