from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings
from PIL import Image
from django.utils.timezone import now



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone, password=None, **extra_fields):
        """Create and save a User with the given phone and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")
    phone = models.CharField(validators = [phoneNumberRegex], max_length = 12, unique = True, verbose_name='Phone Number', blank=False, help_text='WhatsApp Number only !')

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='no-person.png', upload_to='profile_pic')
    account_balance = models.FloatField(default=0)
    approved = models.BooleanField(default = False)
    fullname = models.CharField(max_length=30, blank=False, verbose_name='Full name')
    socialmedia = models.URLField(verbose_name='Social Media URL')

    def firstname(self):
        return self.fullname.split()[0]
    
    def __str__(self):
        return f'{self.fullname.split()[0]}\'s Profile'
    
    def save(self):
        try:
            profile = Profile.objects.get(pk=self.pk)
            if profile.image != self.image:
                profile.image.delete(save=False)
        except Profile.DoesNotExist:
            # Please Ignore
            pass
        
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Withdraw(models.Model):
    amount = models.IntegerField()
    account_number = models.IntegerField()
    date = models.DateTimeField(default=now)
    bank_name = models.CharField(max_length=30)
    account_name = models.CharField(max_length=30)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.profile}'
    
    class Meta:
        ordering = ['-date']