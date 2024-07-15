from django.shortcuts import render, redirect
from .forms import UploadPDFForm
# from django.utils import extract_questions_from_pdf

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_instance = form.save(commit=False)
            pdf_instance.user = request.user
            pdf_instance.save()
            
            # Extract questions from the uploaded PDF
            # extract_questions_from_pdf(pdf_instance)

            return redirect('pdf_upload_success')  # Redirect to a success page
    else:
        form = UploadPDFForm()

    return render(request, 'torque/upload_pdf.html', {'form': form})

def pdf_upload_success(request):
    return render(request, 'torque/pdf_upload_success.html')
