from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Module, Class, Subject, Chapter, Question, Test, TestQuestion
import io
from django.template.loader import get_template
from xhtml2pdf import pisa  # You might need to install xhtml2pdf

@login_required
def module_selection(request):
    modules = Module.objects.all()
    return render(request, 'test_generator/module_selection.html', {'modules': modules})

@login_required
def class_selection(request, module_id):
    module = get_object_or_404(Module, pk=module_id)
    classes = Class.objects.filter(module=module)
    return render(request, 'test_generator/class_selection.html', {'module': module, 'classes': classes})

@login_required
def subject_selection(request, class_id):
    class_model = get_object_or_404(Class, pk=class_id)
    subjects = Subject.objects.filter(class_instance=class_model)
    return render(request, 'test_generator/subject_selection.html', {'class': class_model, 'subjects': subjects})

@login_required
def chapter_selection(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    chapters = Chapter.objects.filter(subject=subject)
    return render(request, 'test_generator/chapter_selection.html', {'subject': subject, 'chapters': chapters})

@login_required
def question_selection(request, chapter_id):
    chapter = get_object_or_404(Chapter, pk=chapter_id)
    questions = Question.objects.filter(chapter=chapter)
    return render(request, 'test_generator/question_selection.html', {'chapter': chapter, 'questions': questions})

@login_required
def create_test(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name')
        is_online = 'is_online' in request.POST
        question_ids = request.POST.getlist('questions')

        test = Test.objects.create(name=test_name, is_online=is_online)

        for question_id in question_ids:
            question = get_object_or_404(Question, pk=question_id)
            TestQuestion.objects.create(test=test, question=question)

        return redirect('test_generator:test_detail', test_id=test.id)

    return render(request, 'test_generator/create_test.html')

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    test_questions = TestQuestion.objects.filter(test=test)
    return render(request, 'test_generator/test_detail.html', {'test': test, 'test_questions': test_questions})

@login_required
def download_test_pdf(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    test_questions = TestQuestion.objects.filter(test=test)
    template_path = 'test_generator/test_pdf.html'
    context = {'test': test, 'test_questions': test_questions}
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{test.name}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("UTF-8")),
        dest=response,
        encoding='UTF-8'
    )

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from django.contrib import messages
@login_required
def add_question(request):
    if request.method == 'POST':
        question_type=request.POST.get('question_type')
        module_id = request.POST.get('module')
        class_id = request.POST.get('class')
        subject_id = request.POST.get('subject')
        chapter_id = request.POST.get('chapter')
        question_text = request.POST.get('question')
        solution_text = request.POST.get('solution')
        max_marks=request.POST.get('max_marks')
        pyq=request.POST.get('pyq')

        module = Module.objects.get(id=module_id)
        class_instance = Class.objects.get(id=class_id)
        subject = Subject.objects.get(id=subject_id)
        chapter = Chapter.objects.get(id=chapter_id)

        question = Question.objects.create(
            question_type=question_type,
            module=module,
            class_instance=class_instance,
            subject=subject,
            chapter=chapter,
            question_text=question_text,
            solution=solution_text,
            added_by_user=request.user,
            max_marks=max_marks,
            pyq=pyq
        )
        messages.success(request, "Question added.")
        return redirect('../add-question')  # Redirect to the same form or another page after submission

    modules = Module.objects.all()
    classes = Class.objects.all()
    subjects = Subject.objects.all()
    chapters = Chapter.objects.all()

    context = {
        'modules': modules,
        'classes': classes,
        'subjects': subjects,
        'chapters': chapters,
    }

    return render(request, 'test_generator/add_question.html', context)