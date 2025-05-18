from django.db import models

# Create your models here.
class Featured(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="featured/")
    url = models.URLField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    is_coming_soon = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class MemeforgeFont(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="fonts/")

    def __str__(self):
        return self.name


class TabiPayCard(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="tabipay/")
    description = models.TextField(blank=True)
    username_x = models.FloatField(null=True, default=450)
    username_y = models.FloatField(null=True, default=900)
    name_x = models.FloatField(null=True, default=450)
    name_y = models.FloatField(null=True, default= 850)
    name_font_size = models.FloatField(null=True, default=50)
    username_font_size = models.FloatField(null=True,default=35)
    font = models.ForeignKey(MemeforgeFont, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return self.title

class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MCQQuestion(models.Model):
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=300)

    def __str__(self):
        return self.question_text

class MCQOption(models.Model):
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.option_text} ({'Correct' if self.is_correct else 'Wrong'})"

