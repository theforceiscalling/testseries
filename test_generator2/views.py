from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Module, Class, Subject, Textbook, Chapter, Question, Test, TestQuestion
import io
from django.template.loader import get_template
from xhtml2pdf import pisa  # You might need to install xhtml2pdf
from django.contrib import messages

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
def textbook_selection(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    textbooks = Textbook.objects.filter(subject=subject)
    return render(request, 'test_generator/textbook_selection.html', {'subject': subject, 'textbooks': textbooks})

@login_required
def chapter_selection(request):
    textbook_ids = request.POST.getlist('textbook_ids')
    textbooks = Textbook.objects.filter(id__in=textbook_ids)
    chapters = Chapter.objects.filter(textbook__in=textbooks)
    return render(request, 'test_generator/chapter_selection.html', {'textbooks': textbooks, 'chapters': chapters})

@login_required
def question_selection(request):
    chapter_ids = request.POST.getlist('chapter_ids')
    chapters = Chapter.objects.filter(id__in=chapter_ids)
    questions = Question.objects.filter(chapter__in=chapters)
    return render(request, 'test_generator/question_selection.html', {'chapters': chapters, 'questions': questions})

@login_required
def create_test(request):
    if request.method == 'POST':
        user = request.user
        test_name = request.POST.get('test_name')
        is_online = 'is_online' in request.POST
        question_ids_str = request.POST.get('questions')
        
        # Handle both comma-separated string and list format
        if isinstance(question_ids_str, str):
            question_ids = list(map(int, question_ids_str.split(',')))
        else:
            question_ids = list(map(int, question_ids_str))
        
        test = Test.objects.create(name=test_name, is_online=is_online, added_by_user=user)

        for question_id in question_ids:
            question = get_object_or_404(Question, pk=question_id)
            TestQuestion.objects.create(test=test, question=question)

        messages.success(request, "Test was created sucessfully! You can download Question and Solutions PDF!")
        return redirect('test_generator:test_detail', test_id=test.id)        
    
    return render(request, 'test_generator/create_test.html')

@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    test_questions = TestQuestion.objects.filter(test=test)
    return render(request, 'test_generator/test_detail.html', {'test': test, 'test_questions': test_questions})

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import io

@login_required
def download_test_pdf(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    test_questions = TestQuestion.objects.filter(test=test)
    template_path = 'test_generator/test_pdf.html'
    context = {'test': test, 'test_questions': test_questions}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{test.name}_test.pdf"'

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

@login_required
def download_solutions_pdf(request, test_id):
    try:
        test = get_object_or_404(Test, pk=test_id)
        test_questions = TestQuestion.objects.filter(test=test)
        template_path = 'test_generator/solutions_pdf.html'
        context = {'test': test, 'test_questions': test_questions}

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{test.name}_solutions.pdf"'

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

    except Exception as e:
        return HttpResponse(f'An error occurred: {e}')


# from django.contrib import messages
# @login_required
# def add_question(request):
#     if request.method == 'POST':
#         question_type=request.POST.get('question_type')
#         module_id = request.POST.get('module')
#         class_id = request.POST.get('class')
#         subject_id = request.POST.get('subject')
#         chapter_id = request.POST.get('chapter')
#         question_text = request.POST.get('question')
#         solution_text = request.POST.get('solution')
#         max_marks=request.POST.get('max_marks')
#         pyq=request.POST.get('pyq')

#         module = Module.objects.get(id=module_id)
#         class_instance = Class.objects.get(id=class_id)
#         subject = Subject.objects.get(id=subject_id)
#         chapter = Chapter.objects.get(id=chapter_id)

#         question = Question.objects.create(
#             question_type=question_type,
#             module=module,
#             class_instance=class_instance,
#             subject=subject,
#             chapter=chapter,
#             question_text=question_text,
#             solution=solution_text,
#             added_by_user=request.user,
#             max_marks=max_marks,
#             pyq=pyq
#         )
#         messages.success(request, "Question added.")
#         return redirect('../add-question')  # Redirect to the same form or another page after submission

#     modules = Module.objects.all()
#     classes = Class.objects.all()
#     subjects = Subject.objects.all()
#     chapters = Chapter.objects.all()

#     context = {
#         'modules': modules,
#         'classes': classes,
#         'subjects': subjects,
#         'chapters': chapters,
#     }

#     return render(request, 'test_generator/add_question.html', context)

@login_required
def my_tests(request):
    user = request.user
    tests = Test.objects.filter(added_by_user=user)
    return render(request, 'test_generator/my_tests.html', {'tests': tests})

from django.shortcuts import render
from .models import Module, Class, Subject, Chapter
from django.http import JsonResponse

def get_classes(request):
    module_id = request.GET.get('module_id')
    classes = Class.objects.filter(module_id=module_id)
    data = [{'id': c.id, 'name': c.name} for c in classes]
    return JsonResponse(data, safe=False)

def get_subjects(request):
    class_id = request.GET.get('class_id')
    subjects = Subject.objects.filter(class_instance_id=class_id)
    data = [{'id': s.id, 'name': s.name} for s in subjects]
    return JsonResponse(data, safe=False)

def get_textbooks(request):
    subject_id = request.GET.get('subject_id')
    textbooks = Textbook.objects.filter(subject_id=subject_id)
    return JsonResponse(list(textbooks.values('id', 'name')), safe=False)

def get_chapters(request):
    textbook_ids = request.GET.getlist('textbook_ids[]')
    chapters = Chapter.objects.filter(textbook_id__in=textbook_ids)
    data = [{'id': c.id, 'name': c.name} for c in chapters]
    return JsonResponse(data, safe=False)

def load_chapters(request):
    textbook_id = request.GET.get('textbook_id')
    chapters = Chapter.objects.filter(textbook_id=textbook_id).all()
    return JsonResponse(list(chapters.values('id', 'title')), safe=False)

def get_questions(request):
    chapter_ids = request.GET.getlist('chapter_ids[]')
    questions = Question.objects.filter(chapter_id__in=chapter_ids)
    data = [{'id': q.id, 'text': q.question_text} for q in questions]
    return JsonResponse(data, safe=False)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Subject

def update_subjects(request, class_id):
    subjects = Subject.objects.filter(class_instance_id=class_id)
    subject_options = '<option value="" disabled selected>Select Subject</option>'
    for subject in subjects:
        subject_options += f'<option value="{subject.id}">{subject.name}</option>'
    data = {
        'subject_options': subject_options
    }
    return JsonResponse(data)

from django.http import JsonResponse

@login_required
def add_question(request):
    if request.method == 'POST':
        question_type = request.POST.get('question_type')
        module_id = request.POST.get('module')
        class_id = request.POST.get('class')
        subject_id = request.POST.get('subject')
        chapter_id = request.POST.get('chapter')
        question_text = request.POST.get('question')
        solution_text = request.POST.get('solution')
        max_marks = request.POST.get('max_marks')
        pyq = request.POST.get('pyq')

        if not all([question_type, module_id, class_id, subject_id, chapter_id, question_text, max_marks]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
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
            return JsonResponse({'success': 'Question added successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
