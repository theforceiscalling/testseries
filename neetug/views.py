from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from .models import neetug_testseries, neetug_testseries_test, neetug_question, neetug_option, TestQuestion, UserResponse, UserScore
from accounts.models import CustomUser

def index(request):
    ts = neetug_testseries.objects.all()
    context = {
        'ts': ts
    }
    return render(request, 'neetug/index.html', context)

@login_required
def testseries_detail(request, slug):
    user_id = request.user.user_id
    user = CustomUser.objects.get(user_id=user_id)
    if neetug_testseries.objects.filter(slug=slug).exists():
        ts = neetug_testseries.objects.filter(slug=slug)
        tss = neetug_testseries.objects.get(slug=slug)
        test = tss.neetug_testseries_test_set.all()
        data = {
            'ts': ts,
            'test': test,
        }
        return render(request, 'neetug/testseries_detail.html', data)

@login_required
def take_test(request, test_code):
    test = get_object_or_404(neetug_testseries_test, code=test_code)
    questions = TestQuestion.objects.filter(test=test).select_related('question').prefetch_related('question__options')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                for question in questions:
                    question_id = question.question.id
                    selected_option_id = request.POST.get(f'question_{question_id}')
                    if selected_option_id:
                        selected_option = get_object_or_404(neetug_option, id=selected_option_id)
                        response, created = UserResponse.objects.get_or_create(
                            user=request.user,
                            test=test,
                            question=question.question,
                            defaults={'selected_option': selected_option}
                        )
                        if not created:
                            response.selected_option = selected_option
                            response.save()

                score = sum(1 for question in questions if UserResponse.objects.get(
                    user=request.user, test=test, question=question.question).selected_option.is_correct)

                UserScore.objects.update_or_create(
                    user=request.user,
                    test=test,
                    defaults={'score': score}
                )
        except IntegrityError:
            return render(request, 'neetug/take_test.html', {'test': test, 'questions': questions, 'error': 'There was an error saving your responses. Please try again.'})
        
        return redirect('score_view', test_id=test.id)

    return render(request, 'neetug/take_test.html', {'test': test, 'questions': questions})

@login_required
def score_view(request, test_id):
    test = get_object_or_404(neetug_testseries_test, pk=test_id)
    user_score = get_object_or_404(UserScore, user=request.user, test=test)
    return render(request, 'neetug/score_view.html', {'test': test, 'score': user_score.score})

def list_questions(request):
    questions = neetug_question.objects.prefetch_related('options').all()
    tests = neetug_testseries_test.objects.all()
    return render(request, 'neetug/list_questions.html', {'questions': questions, 'tests': tests})

@csrf_exempt
@require_POST
def add_to_test(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        question_id = request.POST.get('question_id')
        test_id = request.POST.get('test_id')
        
        try:
            question = get_object_or_404(neetug_question, pk=question_id)
            test = get_object_or_404(neetug_testseries_test, pk=test_id)
            
            if TestQuestion.objects.filter(test=test, question=question).exists():
                return JsonResponse({'success': False, 'error': 'Question already exists in the test'})
            
            TestQuestion.objects.create(test=test, question=question)
            return JsonResponse({'success': True})
        except neetug_question.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Question not found'})
        except neetug_testseries_test.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Test not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})
