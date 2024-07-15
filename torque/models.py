from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedPDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='pdf_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtractedQuestion(models.Model):
    pdf = models.ForeignKey(UploadedPDF, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=50)  # MCQ or Subjective
    options = models.TextField(blank=True, null=True)  # For MCQs
    answer = models.TextField(blank=True, null=True)  # For Subjective
    page_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
