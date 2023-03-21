from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("User must enter a valid email address")
        if not username:
            raise ValueError("User must enter a valid Username")
        
        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password):
        user = self.create_user(        
            email = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name,
            password = password,
        )
        user.is_admin       = True
        user.is_active      = True
        user.is_staff       = True
        user.is_superadmin  = True 
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name      =   models.CharField(max_length=50)
    last_name       =   models.CharField(max_length=50)
    username        =   models.CharField(max_length=500)
    email           =   models.EmailField(unique=True)
    phone_number    =   models.CharField(max_length=50)

    # default_required_fields
    date_joined     =   models.DateTimeField(auto_now_add=True)   
    last_login      =   models.DateTimeField(auto_now_add=True)
    is_admin        =   models.BooleanField(default=False)
    is_staff        =   models.BooleanField(default=False)
    is_active       =   models.BooleanField(default=False)
    is_superadmin   =   models.BooleanField(default=False)

    # this will show the option to enter email instead of username while logging into django admin
    USERNAME_FIELD  =   'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    # this model will know that we are using the MyAccountManager class for creating the user instead of Django defaults.
    object = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

        

    