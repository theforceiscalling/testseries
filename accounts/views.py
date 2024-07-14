from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import CustomUser, user_email_verification_data
from neetug.models import UserScore
from neetug.models import neetug_question, neetug_option
import random
from accounts.decorators import teacher_required

User=get_user_model()

def generate_random_code():
    return ''.join(random.choices('0123456789', k=6))  # Generates random 6 digit code

def index(request):
    if request.user.is_authenticated:
        return redirect('myaccount')
    messages.warning(request, "You need to login first!")
    return redirect('login')

def register_user(request, is_teacher=False):
    if request.method == 'POST':
        print(is_teacher)
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('registerstudent' if not is_teacher else 'registerteacher')
                # print(is_teacher)
            else:
                user = CustomUser.objects.create_user(email=email, password=password1)
                user.save()
                CustomUser.objects.filter(email=email).update(is_teacher=is_teacher, is_student=not is_teacher, is_active=False)
            if not is_teacher:
                code = generate_random_code()
                CustomUser.objects.filter(email=email).update(is_active=False)
                user_email_verification_data.objects.create(user_id=user, verification_code=code)
                # email_message = EmailMessage('TestSeries Verification', f'Your Verification code is: {code}', 'support@testseries.online', [email])
                # email_message.send()
                messages.success(request, "Account created. Check your mailbox for verification mail.")
            else:
                messages.success(request, 'Teacher account created. Proceed to login.')
            return redirect('login')
        messages.info(request, 'Password mismatch!')
        return redirect('registerstudent' if not is_teacher else 'registerteacher')
    return render(request, 'registerstudent.html' if not is_teacher else 'registerteacher.html')

def registerteacher(request):
    return register_user(request, is_teacher=True)

def registerstudent(request):
    return register_user(request, is_teacher=False)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            if not user.is_active:
                messages.warning(request, 'Account not verified. Check your mailbox for verification mail.')
                return redirect('verify')
            else:
                auth_login(request, user)
                return redirect('myaccount')
        else:
            messages.warning(request, 'Invalid combination!')
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def myaccount(request):
    user_scores = UserScore.objects.filter(user=request.user)
    context = {'test_scores': user_scores}
    return render(request, 'myaccount.html', context)

def verify(request):
    if request.method == "POST":
        email = request.POST['email']
        code = request.POST['verification_code']
        try:
            user = CustomUser.objects.get(email=email)
            if user is not None:
                verification_data = user_email_verification_data.objects.get(user_id=user)
                verification_code = verification_data.verification_code
                if code == verification_code:
                    CustomUser.objects.filter(email=email).update(is_active = True)
                    messages.success(request, "Account successfully verified! You can login now.")
                    return redirect('login')
                else:
                    messages.warning(request, "Verification failed!")
                    return redirect('verify')
            else:
                messages.warning(request, "This account does not exist.")
                return redirect('verify')
        except user_email_verification_data.DoesNotExist:
            messages.warning(request, "Verification failed!")
            return redirect('verify')
    return render(request, 'verify.html')

@teacher_required
def addquestion(request):
    if request.method == "POST":
        data = request.POST
        correct_option = data['correct_option']
        create_question = neetug_question.objects.create(
            question_type="MCQ",
            subject=data['subject'],
            from_class=data['class'],
            chapter=data['chapter'],
            topic=data['topic'],
            question_text=data['question'],
            description=data['description'],
            diagram_or_illustration=data['diagram'],
            pyq_Last_asked_in=data['pyq_year'],
            question_code=generate_random_code()
        )
        for i in range(1, 5):
            neetug_option.objects.create(
                question=create_question,
                option=data[f'option_{i}'],
                is_correct=(correct_option == f'option_{i}')
            )
        messages.success(request, "Question has been added.")
        return render(request, 'addquestion.html')
    return render(request, 'addquestion.html')

@login_required
def addquestion_to_test(request):
    questions = neetug_question.objects.prefetch_related('options').all()
    return render(request, "addquestion_to_test.html", {'questions': questions})

def unauthorized_access(request):
    return render(request, 'accounts/unauthorized.html')