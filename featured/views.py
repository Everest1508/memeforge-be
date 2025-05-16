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
        

import io
from django.http import HttpResponse, Http404
from PIL import Image, ImageDraw, ImageFont
from users.models import UserTabiPayCardOverlay

from django.conf import settings
import os

def serve_tabipay_image(request, uuid):
    try:
        overlay = UserTabiPayCardOverlay.objects.select_related('card').get(uuid=uuid)
    except UserTabiPayCardOverlay.DoesNotExist:
        raise Http404("Card not found")

    card_image_path = overlay.card.image.path
    try:
        image = Image.open(card_image_path).convert("RGBA")
    except Exception:
        raise Http404("Image not found or unreadable")

    # Draw on image
    draw = ImageDraw.Draw(image)
    
    # Use default font or provide a TTF path
    font_path = os.path.join(settings.BASE_DIR, "arial.ttf")  # Place the font in BASE_DIR
    font = ImageFont.truetype(font_path, size=36)

    draw.text((30, 30), f"@{overlay.username}", fill="white", font=font)
    draw.text((30, 80), overlay.name, fill="white", font=font)

    # Save to memory and return
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")
