from django import forms
from .models import Question
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from django.core.exceptions import ValidationError
from .models import is_paraphrase

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['module', 'class_instance', 'subject', 'chapter', 'question_text', 'question_type', 'solution', 'options']
        widgets = {
            'question_type': forms.RadioSelect(choices=[('MCQ', 'MCQ'), ('Subjective', 'Subjective')]),
            'options': forms.Textarea(attrs={'rows': 3, 'placeholder': 'For MCQs, enter options separated by commas'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        question_text = cleaned_data.get('question_text')

        print(f"Checking question text: {question_text}")

        if Question.objects.filter(question_text=question_text).exists():
            self.add_error('question_text', 'A question with the same text already exists.')

        if is_paraphrase(question_text):
            self.add_error('question_text', 'A paraphrased version of this question already exists.')

        return cleaned_data
