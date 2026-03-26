from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager



# Create your models here.

class TeacherManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(email,password,**extra_fields)

class Teacher(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TeacherManager()
    def __str__(self):
        return self.email









