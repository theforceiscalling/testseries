from django.urls import path
from . import views

app_name = 'test_generator'

urlpatterns = [
    path('modules/', views.module_selection, name='module_selection'),
    path('classes/<int:module_id>/', views.class_selection, name='class_selection'),
    path('subjects/<int:class_id>/', views.subject_selection, name='subject_selection'),
    path('chapters/<int:subject_id>/', views.chapter_selection, name='chapter_selection'),
    path('questions/<int:chapter_id>/', views.question_selection, name='question_selection'),
    path('create_test/', views.create_test, name='create_test'),
    path('test_detail/<int:test_id>/', views.test_detail, name='test_detail'),
    path('download_test_pdf/<int:test_id>/', views.download_test_pdf, name='download_test_pdf'),
    path('add-question/', views.add_question, name='add_question'),
]
