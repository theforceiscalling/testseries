from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class Exam(models.Model):
    exam_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    exam_code = models.CharField(max_length=10)
    # description = models.CharField(max_length=100000)
    description = HTMLField(max_length=5000)
    latest_updates = models.CharField(max_length=5000)
    exam_added_on = models.DateTimeField(auto_now_add=True)
    exam_last_updated_on = models.DateTimeField(auto_now=True)