from django.contrib import admin
from .models import *
# Register your models here.

class TestQuestionAdmin(admin.ModelAdmin):
     list_display=("test", "question")

class UserResponseAdmin(admin.ModelAdmin):
     list_display=("user", "test")

class UserScoreAdmin(admin.ModelAdmin):
     list_display=("user", "test", "score")

class neetug_testseriesAdmin(admin.ModelAdmin):
     list_display=("name", "code", "valid_till")
     
class neetug_testseries_testAdmin(admin.ModelAdmin):
    list_display=("name", "code", "maximum_marks")
     
class neetug_questionAdmin(admin.ModelAdmin):
     list_display=("question_text", "subject", "from_class")

class neetug_optionAdmin(admin.ModelAdmin):
     list_display=("option", "is_correct")
     
admin.site.register(neetug_testseries, neetug_testseriesAdmin)
admin.site.register(neetug_testseries_test, neetug_testseries_testAdmin)
admin.site.register(neetug_question, neetug_questionAdmin)
admin.site.register(neetug_option, neetug_optionAdmin)
admin.site.register(TestQuestion, TestQuestionAdmin)
admin.site.register(UserResponse, UserResponseAdmin)
admin.site.register(UserScore, UserScoreAdmin)