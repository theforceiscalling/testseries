# accounts/decorators.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

def teacher_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_teacher or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You do not have permission to access this page.")
                return redirect(reverse('unauthorized'))
        else:
            return redirect(f'{reverse("login")}?next={request.path}')
    return _wrapped_view_func
