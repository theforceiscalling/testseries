from django.shortcuts import render
from neetug import models
from models import nt26001
# Create your views here.
def index(request):
    if request.method == "POST":
        test = nt26001.objects.all()
        test.questions
        return render(request, 'taketest/index.html')
    else:
        return render(request, 'taketest/index.html')
    
