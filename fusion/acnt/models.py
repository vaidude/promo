

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_("Email"),max_length=255,unique=True,)
    first_name = models.CharField(max_length=50 ,verbose_name=_("First Name"))
    last_name = models.CharField(max_length=50 ,verbose_name=_("Last Name"))
    is_freelancer = models.BooleanField(default = False )
    is_client = models.BooleanField(default =False )
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    is_verified = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name"]

    objects = UserManager()


    def save(self, *args, **kwargs):
        # Ensure either is_freelancer or is_client is set, but not both
        if self.is_freelancer and self.is_client:
            raise ValueError("A user cannot be both a freelancer and a client.")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.email}"
    
    def get_full_name(self):
        return f"{self.first_name}{self.last_name}"
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
    }

    # Rest of your User model fields and methods...

class Client(models.Model):
    user = models.OneToOneField(User, related_name="client", on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )
    phone = models.CharField(max_length=10, validators=[phone_regex], blank=True, null=True)
    address = models.CharField(max_length=50, default='')
    about = models.TextField()
    
    def __str__(self):
        return self.user.email
    def __str__(self):
        return self.user.get_full_name
    

    # Rest of your Client model fields...

  # Rest of your JobNames model fields...
class JobNames(models.Model):
    jobcategory = models.CharField(max_length=50, default='')

class Freelancer(models.Model):
    user = models.OneToOneField(User, related_name="freelancer", on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profile_photos', blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be a 10-digit number."
    )
    phone = models.CharField(max_length=10, validators=[phone_regex], blank=True, null=True)
    job = models.ForeignKey(JobNames, on_delete=models.CASCADE,null=True)
    address = models.CharField(max_length=250, default='')
    rating = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    EXPERIENCE_CHOICES = (
    ('Entry Level', 'Entry Level'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
   )

    experiance = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Entry Level')
    age = models.PositiveIntegerField(default=0)
    about = models.TextField(default='')
    price = models.PositiveIntegerField(default=0)
    portfolio = models.URLField(max_length=200, blank=True, null=True)
    availability = models.BooleanField(default=True)
    
    # Rest of your Freelancer model fields...



  