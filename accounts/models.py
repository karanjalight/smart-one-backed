from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import CustomUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUser(AbstractBaseUser, PermissionsMixin):
    #remove comments when cloning a fresh
#    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField('Full Name' ,max_length=300, null=True )
    name = models.CharField(max_length=150, null=True)
    phone_number = models.CharField(max_length=15, null=True, verbose_name="Enter Phone Number")
    about_you = models.CharField(max_length=300, null=True )
    is_restaurant = models.BooleanField(default=False)                          #============= Account associated with restaurant
    is_admin = models.BooleanField(default=False, verbose_name="admin rights")  #============= Give admin rights to staff
    is_staff = models.BooleanField(default=False)                               #============= Employee 
    is_customer = models.BooleanField(default=False)                            #============= for the customer
    is_driver = models.BooleanField(default=False)                              #============= for the driver app
    is_active = models.BooleanField(default=True)                               #============= this revokes a users access
    date_joined = models.DateTimeField(default=timezone.now)
    verification_code = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=False, null=True, blank=True)
    time_available = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    affiliate_code = models.CharField(max_length=300, null=True, unique=True, blank=True)
    is_affiliate = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
