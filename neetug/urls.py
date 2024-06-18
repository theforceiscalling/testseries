from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='neetug_homepage'),
    path('testseries/<slug>', views.testseries_detail, name='neetug_testseries-detail'),
    path('take_test/<int:test_code>/', views.take_test, name='take_test'),
    path('score/<int:test_id>/', views.score_view, name='score_view'),
    path('list_questions', views.list_questions, name='list_questions'),
    path('add_to_test', views.add_to_test, name='add_to_test'),
    # path('take_test/<int:test_id>/', views.take_test, name='take_test'),
    # path('submit_test/<int:test_id>/', views.submit_test, name='submit_test'),
]