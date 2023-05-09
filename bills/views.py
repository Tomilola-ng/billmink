import requests
from .utils import month
from django.urls import reverse
from django.conf import settings
from .models import Bill, Activity
from django.contrib import messages
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def activity(request):
    obj = Activity.objects.filter(profile = request.user.profile)
    
    context = {
        'obj': obj,
    }

    return render(request, 'accounts/activity.html', context)

class billCreate(LoginRequiredMixin , CreateView):
    model = Bill
    fields = ['amount', 'bill_type', 'currency']

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formname'] = 'Create Bill'
        return context 

    def form_valid(self, form):
        form.instance.user = self.request.user

        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f' Created a {form.instance.amount} {form.instance.bill_type}'
        acc.save()
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index_view')


class billUpdate(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Bill
    fields = ['bill_type', 'amount']

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f' Updated the { self.object }'
        acc.save()

        return super().form_valid(form)

    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False

    def get_success_url(self):
        return reverse('index_view')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formname'] = 'Update Bill'
        return context 
        

class billDelete(LoginRequiredMixin, UserPassesTestMixin ,DeleteView):

    model = Bill
    template_name = 'bills/confirm.html'

    def get_success_url(self):
        return reverse('index_view')
        
    def form_valid(self, form):
        success_url = self.get_success_url()
        
        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f' Deleted the {self.object }'
        acc.save()

        self.object.delete()
        return HttpResponseRedirect(success_url)
    
    def test_func(self):
        profile = self.get_object()
        if self.request.user == profile.user:
            return True
        return False



#  Involves Bill pAying
def bill_pay(request, id):
    bill = get_object_or_404(Bill, id = id)

    context = {
        'bill': bill,
        'public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'bills/payment.html', context)


@csrf_exempt
def update_bill(request):
    if request.method == 'POST':
        bill_id = request.POST.get('bill_id')
        payer_email = request.POST.get('payerEmail')
        reference = request.POST.get('reference')

        try:
            # Look up Bill object with provided ID
            bill = Bill.objects.get(id=bill_id)
        except Bill.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Invalid Bill ID'})

        headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
        url = f'https://api.paystack.co/transaction/verify/{reference}'
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            # Payment validation failed due to API error
            return JsonResponse({'success': False, 'error_message': 'Payment verification failed'})

        # Parse response from Paystack API
        data = response.json()

        if not data['status']:
            # Payment validation failed
            return JsonResponse({'success': False, 'error_message': 'Payment verification failed'})

        # Check that payment amount matches expected amount
        expected_amount = bill.amount * 100 # Paystack API uses kobo instead of naira
        if data['data']['amount'] != expected_amount:
            # Payment amount does not match expected amount
            bill.user.profile.account_balance = bill.user.profile.account_balance  + expected_amount / 100  # Convert kobo to naira
            bill.user.profile.save()
            return JsonResponse({'success': False, 'error_message': 'Payment amount does not match expected amount'})

        # Update Bill object as paid
        bill.paid = True
        bill.paid_by = payer_email
        bill.save()

        # Return success message as JSON response
        return JsonResponse({'success': True})

    # Return error message as JSON response
    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})
