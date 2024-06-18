from django.db import models
from neetug.models import neetug_testseries_test
# Create your models here.

class nt26001(models.Model):
    test = neetug_testseries_test.objects.filter(code="nt26001")
    questions = models.CharField(max_length=50000, default="", )
    added_on = models.DateTimeField(auto_now_add=True)
    last_updated_on = models.DateTimeField(auto_now=True)


    
    
    