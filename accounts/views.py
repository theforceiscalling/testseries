from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .models import CustomUser, user_email_verification_data, account_convert
from neetug.models import UserScore
from neetug.models import neetug_question, neetug_option
import random
from accounts.decorators import teacher_required
from django.core.files.storage import default_storage

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
                CustomUser.objects.filter(email=email).update(is_teacher=is_teacher, is_student=not is_teacher)
                code = generate_random_code()
                user_email_verification_data.objects.create(user_id=user, verification_code=code)
                # email_message = EmailMessage('TestSeries Verification', f'Your Verification code is: {code}', 'support@testseries.online', [email])
                # email_message.send()
                messages.success(request, "Account created. Check your mailbox for verification mail.")
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

@login_required
def account_convert_request(request):
    if request.user.is_teacher or request.user.is_superuser:
        messages.warning(request, "You already have a teacher account. If you convert this account to Student account, you will not be able to convert it back to teacher account in future. Please, make sure you are aware of this.")
    elif request.user.is_student or request.user.is_superuser:
        messages.warning(request, "Dear User, You have a Student Account, and you are requesting for converting your student account into a teacher account. This change is irreversible.")
        if request.method == "POST":
            email = request.user.email
            CustomUser.objects.filter(email=email).update(is_teacher=True, is_student=False)
            messages.success(request, "Your account has been converted successfully.")
            # current_account_type = request.POST['current_account_type']
            # requested_account_type = request.POST['requested_account_type']
            # id_proof = request.FILES['id_proof']
            # get_request = account_convert.objects.create(user=request.user, current_account_type=current_account_type, requested_account_type=requested_account_type, id_proof=id_proof)
            # get_request.save
            # messages.success(request, "Your request has been submitted which is subjected to approval for authenticity.")
            # messages.info(request, "You will receive an email in your inbox (or spam in some cases) as soon as your account migration is completed. In case you do not hear from us in 48 hours, kindly contact our support team.")
            
    else:
        messages.warning(request, "An error was encountered. Error Code: #29848. Contact support team with this code for quick guidance.")        
        
    return render(request, 'account_convert_request.html')

from test_generator2.models import Question

@teacher_required
def questions_added_by_me(request):
    ques = Question.objects.filter(added_by_user=request.user)
    
    context = {
        'ques': ques
    }
    
    return render(request, 'questions_added_by_me.html', context)