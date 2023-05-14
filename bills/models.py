import uuid
import secrets
from django.db import models
from .paystack import Paystack
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from accounts.models import Profile
from .choices import bill_types, currency_types

User = settings.AUTH_USER_MODEL

class Bill(models.Model):
    id = models.UUIDField(default = uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=100)
    Description = models.TextField(verbose_name="Bill Description", default='Payment bill')
    bill_type = models.CharField(
        choices = bill_types, 
        default='Web-design', 
        max_length=50, 
        verbose_name='Type of bill')
    currency = models.CharField(
        choices = currency_types, 
        default='NGN', 
        max_length=50, 
        verbose_name='Currency')
    paid_by = models.CharField(default='No One', max_length=100)
    date = models.DateTimeField(default = timezone.now )
    paid = models.BooleanField(default=False)

    
    class Meta:
        ordering = ['-date']

    def get_absolute_url(self) -> str:
        return reverse('index_view')

    def ref(self):
        return secrets.token_urlsafe(50)
    
    def amount_value(self) -> int:
        return self.amount * 100

    def symbol(self):
        if self.currency == 'USD':
            return '$'
        return '₦'

    def __str__(self) -> str:
        return f'{self.symbol()}{self.amount} {self.bill_type}'

    def status(self) -> str:
        if self.paid:
            return 'Paid' 
        else:
            return 'Pending' 

    def link(self):
        return f'http://{settings.DOMAIN_PATH}/bill/{self.id}/payment/' 
    
    def payment_verify(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)

        if status:
            if result['amount'] / 100 == self.amount:
                self.paid = True
            self.save()
        if self.paid:
            return True
        return False


class Activity(models.Model):
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f'{ self.description }'
    
    class Meta:
        ordering = ['-date']