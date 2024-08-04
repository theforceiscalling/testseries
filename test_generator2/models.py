from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
import spacy
from sklearn.metrics.pairwise import cosine_similarity

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
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
nlp = spacy.load('en_core_web_md')

def is_paraphrase(new_question_text):
    new_question_doc = nlp(new_question_text)
    existing_questions = Question.objects.all()

    print(f"New question doc: {new_question_doc}")

    for question in existing_questions:
        existing_question_doc = nlp(question.question_text)
        similarity = new_question_doc.similarity(existing_question_doc)
        
        print(f"Comparing with existing question: {question.question_text}")
        print(f"Similarity: {similarity}")
        
        if similarity > 0.9:  # Adjust threshold as needed
            return True
    return False


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
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, null=True, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    question_text = models.TextField()
    question_diagram_or_illustration = models.FileField(upload_to="test_generator2/", max_length=250, null=True, blank=True)
    solution = models.TextField(blank=True, null=True)
    solution_diagram_or_illustration = models.FileField(upload_to="test_generator2/", max_length=250, null=True, blank=True)
    max_marks = models.IntegerField(default=0)
    added_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pyq = models.CharField(max_length=20, blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    
    def save(self, *args, **kwargs):
        if Question.objects.filter(question_text=self.question_text).exists():
            raise ValidationError('A question with the same text already exists.')
        if is_paraphrase(self.question_text):
            raise ValidationError('A paraphrased version of this question already exists.')
        super(Question, self).save(*args, **kwargs)
    
class Test(models.Model):
    name = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    added_by_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    test_instructions = models.CharField(max_length=5000, default=None, null=True, blank=True)
    test_time_in_minutes = models.IntegerField(default=60)
    watermark_text = models.CharField(max_length=50, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class TestQuestion(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, null=True, blank=True)
    section = models.CharField(max_length=10, default=None, null=True, blank=True)

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
