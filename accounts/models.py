from django.db import models
import random
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

code = ''.join(random.choices('0123456789', k=6)) #Generates random 6 digit code
print(code)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # username = str("student"+phone_number)
        # user = self.model(email=email)
        # user = self.model(username=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=50, null=True) #Email
    phone_number = models.CharField(max_length=15) #phone number
    username = models.CharField(max_length=10, unique=True, null=True, default=None)
    temp_token = models.CharField(max_length=10, default="3761") #Can be used to store OTP/Temp Tokens/Verification
    testseries = models.CharField(max_length=100, default='') #tells which testseries' user is enrolled into, it must contain only the testseries codes
    is_student = models.BooleanField(default=False) #gives students permissions
    is_teacher = models.BooleanField(default=False) #gives teacher permissions
    subscription = models.CharField(max_length=8, default="INACTIVE") #plus subscription is active or inactive
    is_active = models.BooleanField(default=False)  # Ensure is_active is present
    is_staff = models.BooleanField(default=False)  # Ensure is_staff is present
    form_token = models.CharField(max_length=50, default='')  # Ensure is_staff is present
    full_name = models.CharField(max_length=100, default="", null=True)
    account_status = models.CharField(max_length=10, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
    
    def __str__(self):
        return self.email

class user_email_verification_data(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=10, default="")
    first_record_created_on = models.DateTimeField(auto_now_add=True)
    latest_record_created_on = models.DateTimeField(auto_now=True)

class account_convert(models.Model):
    request_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    current_account_type = models.CharField(max_length=10, default="")
    requested_account_type = models.CharField(max_length=10, default="")
    request_status = models.CharField(max_length=10, default="Pending", choices=[
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
    ])
    declined_reason = models.CharField(max_length=500, default="Pending", choices=[
        ('Identity Proof Expired', 'Identity Proof Expired'),
        ('Invalid ID', 'Invalid ID'),
        ('Uploaded ID is not clear' , 'Uploaded ID is not clear'),
        ('Full Identity was not uploaded' , 'Full Identity was not uploaded'),
        ('Photo not clear in Identity', 'Photo not clear in Identity'),
        ('Mobile number not available in Identity','Mobile number not available in Identity'),
        ('Violation of Policy', 'Violation of Policy')
    ])
    id_proof = models.FileField(upload_to="id_proofs/", default=None, blank=False)
    added_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    temp_field = models.CharField(max_length=10, default="temp")
