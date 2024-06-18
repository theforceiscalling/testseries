# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, user_email_verification_data

# # Register your models here.

# admin.site.register(CustomUser, UserAdmin)

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin

class user_email_verification_dataAdmin(admin.ModelAdmin):
     list_display=("user_id", "verification_code")

class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'phone_number', 'is_active', 'subscription', 'testseries')
    list_filter = ['username', 'email']

    fieldsets = (
        (None, {'fields': ('username', 'email','password')}),

        ('Permissions', {'fields': ('is_superuser',)}),
    )

    search_fields =  ('email', 'username')
    ordering = ('email', 'username')

    filter_horizontal = ()

admin.site.register(CustomUser,UserAdmin)
admin.site.register(user_email_verification_data,user_email_verification_dataAdmin)