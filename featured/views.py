# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Featured, TabiPayCard, QuestionCategory, MCQQuestion, MCQOption
from .serializers import (
    FeaturedSerializer, TabiPayCardSerializer, 
    MCQQuestionSerializer
)
import random

class FeaturedListView(generics.ListAPIView):
    queryset = Featured.objects.all().order_by('order')
    serializer_class = FeaturedSerializer

class TabiPayCardListView(generics.ListAPIView):
    queryset = TabiPayCard.objects.all()
    serializer_class = TabiPayCardSerializer

class RandomMCQByCategory(APIView):
    def get(self, request, category_id):
        questions = MCQQuestion.objects.filter(category_id=category_id)
        random_questions = random.sample(list(questions), min(3, questions.count()))
        serializer = MCQQuestionSerializer(random_questions, many=True)
        return Response(serializer.data)

class CheckMCQAnswer(APIView):
    def post(self, request):
        data = request.data
        try:
            option = MCQOption.objects.get(id=data['selected_option_id'], question_id=data['question_id'])
            return Response({
                'correct': option.is_correct
            })
        except MCQOption.DoesNotExist:
            return Response({'error': 'Invalid question or option.'}, status=status.HTTP_400_BAD_REQUEST)