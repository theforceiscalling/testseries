# forms.py in test_generator app
from django import forms
from .models import Question

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['module', 'class_instance', 'subject', 'chapter', 'question_text', 'question_type', 'solution_text', 'options']
        widgets = {
            'question_type': forms.RadioSelect(choices=[('MCQ', 'MCQ'), ('Subjective', 'Subjective')]),
            'options': forms.Textarea(attrs={'rows': 3, 'placeholder': 'For MCQs, enter options separated by commas'}),
        }
