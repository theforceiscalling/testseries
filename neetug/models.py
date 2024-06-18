from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# Create your models here.
class neetug_testseries(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=5000)
    instructions = models.CharField(max_length=5000)
    fees = models.CharField(max_length=10)
    start_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    premium = models.BooleanField(default=True)
    valid_till = models.DateTimeField()
    remark = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True, null=True, default=None)
    
    def __str__(self):
        return f""+self.name+" ("+self.code+")"
    
class neetug_testseries_test(models.Model):
    testseries = models.ForeignKey(neetug_testseries, on_delete=models.CASCADE)
    test_date = models.DateTimeField()
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    syllabus = HTMLField(max_length=5000)
    maximum_marks = models.CharField(max_length=5)
    negative_marking = models.BooleanField(default=False)
    marks_per_correct_answer = models.IntegerField()
    marks_per_wrong_answer = models.IntegerField()
    total_questions = models.IntegerField()
    remark = models.CharField(max_length=100)
    exam_questions = models.CharField(max_length=100000, default="", null=True)
    
    def __str__(self):
        return f""+self.name+" ("+self.code+")"
import random 
def generate_random_code():
    return ''.join(random.choices('0123456789', k=6))

class neetug_question(models.Model):
    import random
    rand_code = ''.join(random.choices('0123456789', k=6)) #Generates random 6 digit code
    years = list(range(2024, 1900, -1))

    # Define the choices
    year_choices = [(year, year) for year in years]

    question_type = models.CharField(max_length=10, choices=[
        ('MCQ', 'MCQ'),
    ], default="MCQ")
    subject = models.CharField(max_length=10, default="", choices=[
        ('BIOLOGY', 'BIOLOGY'),
        ('PHYSICS', 'PHYSICS'),
        ('CHEMISTRY', 'CHEMISTRY')
    ])
    from_class = models.CharField(max_length=10, default="", choices=[
        ('Class 11', 'Class 11'),
        ('Class 12', 'Class 12'),
    ])
    chapter = models.CharField(max_length=50, default="")
    topic = models.CharField(max_length=50, default="", null=True, blank=True)
    question_text = models.CharField(max_length=255)
    description = HTMLField(max_length=5000, default="", null=True, blank=True)
    diagram_or_illustration = models.FileField(upload_to=__name__+"/", max_length=250, default=None, null=True, blank=True)
    pyq_Last_asked_in = models.CharField(max_length=4, null=True, blank=True)
    question_code = models.CharField(max_length=10, null=True, blank=True, default=generate_random_code)
    def __str__(self):
        return self.question_text

class neetug_option(models.Model):
    question = models.ForeignKey(neetug_question, related_name='options', on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
class TestQuestion(models.Model):
    test = models.ForeignKey(neetug_testseries_test, on_delete=models.CASCADE)
    question = models.ForeignKey(neetug_question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('test', 'question')
        
    def __str__(self):
        return f""+self.test.name+" ("+self.question.question_text+")"

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(neetug_testseries_test, on_delete=models.CASCADE)
    question = models.ForeignKey(neetug_question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(neetug_option, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'test', 'question')
    
    def __str__(self):
        return f""+self.test.name+")"

class UserScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(neetug_testseries_test, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'test')
        
    def __str__(self):
        return f""+self.test.name+ str(self.score)+""