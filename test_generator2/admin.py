from django.contrib import admin
from .models import *
# Register your models here.

class ModuleAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class ClassAdmin(admin.ModelAdmin):
    list_display=("pk", "name", "module")
    
class SubjectAdmin(admin.ModelAdmin):
    list_display=("pk", "name", "class_instance", "module")

class TextbookAdmin(admin.ModelAdmin):
    list_display=("pk", "name", "subject")
    
class ChapterAdmin(admin.ModelAdmin):
    list_display=("pk", "name", "subject", "textbook")
    
class QuestionAdmin(admin.ModelAdmin):
    list_display=("question_type", "question_text", "class_instance")
    
class TestAdmin(admin.ModelAdmin):
    list_display=("pk", "name")
    
class TestQuestionAdmin(admin.ModelAdmin):
    list_display=("test", "question")
    
class TeacherAdmin(admin.ModelAdmin):
    list_display=("pk", "user")
    
admin.site.register(Module, ModuleAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Textbook, TextbookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(Teacher, TeacherAdmin)
