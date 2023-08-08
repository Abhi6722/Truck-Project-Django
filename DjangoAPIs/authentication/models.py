from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .model_fields import LowercaseEmailField

# from django.contrib.auth.models import User 


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, password=None, password2=None):
        """
        Creates and saves a User with the given email, first_name, last_name and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            # country_code = country_code,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone_number, password=None):
        user = self.create_user(
            email = email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            # country_code = country_code,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = LowercaseEmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # phone_number = PhoneNumberField()
    
    # country_code = models.CharField(max_length=4, default='+91')
    phone_regex = RegexValidator(regex=r'\d{10}', message="Please recheck your phone number")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True) # Validators should be a list
    # otp = models.CharField(max_length = 6,null=True,blank=True)
    
    # is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    

class PhoneOTP(models.Model):
    phone = models.ForeignKey(User, on_delete=models.CASCADE, to_field="phone_number")
    otp = models.CharField(max_length=6, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    validated = models.BooleanField(default=False, help_text='If it is true, that means user have validate otp correctly in second API')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.phone}: {self.otp}"