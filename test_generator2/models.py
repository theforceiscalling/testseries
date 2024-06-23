from django.db import models
from accounts.models import CustomUser

class Module(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Class(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=1)

    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Textbook(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Question(models.Model):
    QUESTION_TYPES = [
        ('theory', 'Theory'),
        ('mcq', 'MCQ'),
        ('assertion_reason', 'Assertion and Reason'),
        ('competency_case', 'Competency/Case Based'),
    ]

    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='theory')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='questions')
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    question_text = models.TextField()
    solution = models.TextField(blank=True, null=True)
    max_marks = models.IntegerField(default=0)
    added_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pyq = models.CharField(max_length=20, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    
class Test(models.Model):
    name = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    added_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Other fields for the teacher