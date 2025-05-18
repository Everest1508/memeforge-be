# views.py
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import Featured, TabiPayCard, MCQQuestion, MCQOption
from .serializers import (
    FeaturedSerializer, TabiPayCardSerializer, 
    MCQQuestionSerializer
)
import random
import io
from django.http import HttpResponse, Http404
from PIL import Image, ImageDraw, ImageFont
from users.models import UserTabiPayCardOverlay
from django.conf import settings
import os
from users.utils import get_user

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


def serve_tabipay_image(request, uuid):
    try:
        overlay = UserTabiPayCardOverlay.objects.select_related('card').get(id=uuid)
    except UserTabiPayCardOverlay.DoesNotExist:
        raise Http404("Card not found")

    card = overlay.card
    card_image_path = card.image.path

    try:
        image = Image.open(card_image_path).convert("RGBA")
    except Exception:
        raise Http404("Image not found or unreadable")

    draw = ImageDraw.Draw(image)

    font_path = card.font.file.path if card.font else os.path.join(settings.BASE_DIR, "static/fonts/Gelline.otf")

    username_font = ImageFont.truetype(font_path, size=card.username_font_size)
    name_font = ImageFont.truetype(font_path, size=card.name_font_size)

    def draw_text_with_border(draw, position, text, font, fill, border_color="black", border_width=2):
        x, y = position
        for dx in [-border_width, 0, border_width]:
            for dy in [-border_width, 0, border_width]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=border_color)
        draw.text((x, y), text, font=font, fill=fill)

    draw_text_with_border(draw, (card.username_x, card.username_y), f"@{overlay.username_text}", username_font, fill="white")
    draw_text_with_border(draw, (card.name_x, card.name_y), overlay.name_text, name_font, fill="white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")


from .serializers import TabiPayCardSerializer
import random

class RandomOrCreateTabiPayOverlay(APIView):

    def get(self, request):
        cards = list(TabiPayCard.objects.all())
        if not cards:
            return Response({"error": "No cards available."}, status=status.HTTP_404_NOT_FOUND)

        card = random.choice(cards)
        serializer = TabiPayCardSerializer(card)
        return Response(serializer.data)

    def post(self, request):
        username_text = request.data.get("username_text")
        name_text = request.data.get("name_text")

        if not username_text or not name_text:
            return Response({"error": "username_text and name_text are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        cards = list(TabiPayCard.objects.all())
        if not cards:
            return Response({"error": "No cards available."}, status=status.HTTP_404_NOT_FOUND)

        card = random.choice(cards)

        user, _ = get_user(request=request)

        if user:
            recent_overlay = UserTabiPayCardOverlay.objects.filter(
                user=user,
                card=card,
                created_at__gte=timezone.now() - timedelta(days=7)
            ).first()

            if recent_overlay:
                return Response({
                    "error": "You can only create this card once every 7 days.",
                    "overlay_id": str(recent_overlay.id),
                    "created_at": recent_overlay.created_at
                }, status=status.HTTP_429_TOO_MANY_REQUESTS)

        overlay = UserTabiPayCardOverlay.objects.create(
            card=card,
            user=user,
            username_text=username_text,
            name_text=name_text
        )

        return Response({
            "overlay_id": str(overlay.id),
            "card_id": card.id,
            "card_title": card.title,
            "username_text": overlay.username_text,
            "name_text": overlay.name_text,
            "created_at": overlay.created_at
        }, status=status.HTTP_201_CREATED)