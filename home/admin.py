from django.contrib import admin
from .models import Exam
# Register your models here.

class ExamAdmin(admin.ModelAdmin):
     list_display=("exam_name", "exam_code")

admin.site.register(Exam, ExamAdmin)