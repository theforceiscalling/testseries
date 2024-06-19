from django.contrib import admin
from .models import *
# Register your models here.

class ModuleAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class ClassAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class SubjectAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class ChapterAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class QuestionAdmin(admin.ModelAdmin):
    list_display=("question_type", "question_text")
    
class TestAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class TestQuestionAdmin(admin.ModelAdmin):
    list_display=("test", "question")
    
class TeacherAdmin(admin.ModelAdmin):
    list_display=("pk", "user")
    
admin.site.register(Module, ModuleAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(Teacher, TeacherAdmin)
