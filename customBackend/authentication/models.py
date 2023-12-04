from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.


REGULAR_ALPHANUM = RegexValidator(r'^[a-zA-Z0-9]*$')


class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None):
        if username is None:
            raise TypeError('Users always should have an username')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password must be provided')
    
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=128, validators=[REGULAR_ALPHANUM], blank=False, unique=True, db_index=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    password = models.CharField(max_length=128, validators=[REGULAR_ALPHANUM], blank=False)
    picture = models.ImageField(upload_to = 'img', blank=True, null=True)
    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.username}"

    def tokens(self):
        user_tokens = RefreshToken.for_user(self)
        return {
            'refresh': str(user_tokens),
            'access': str(user_tokens.access_token),
        }