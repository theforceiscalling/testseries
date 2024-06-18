from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
# from django.contrib.messages import constants as messages
from .models import Exam
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def index(request):
    exam = Exam.objects.all()
    exam_detail = {
        'exam': exam,    
    }
    return render(request, 'index.html', exam_detail)

def error_404(request, exception):
    return render(request, '404.html', status=404)