import uuid
import secrets
from django.db import models
from bills.paystack import Paystack
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
from .choices import gift_types
from bills.choices import currency_types

User = settings.AUTH_USER_MODEL

class Gift(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=100)
    message = models.TextField()
    description = models.TextField()
    gift_type = models.CharField(
        choices = gift_types, 
        default='Support', 
        max_length=20, 
        verbose_name='Gift category')
    currency = models.CharField(
        choices = currency_types, 
        default='NGN', 
        max_length=50, 
        verbose_name='Currency')
    clicks = models.IntegerField()
    date = models.DateTimeField(default = timezone.now )

