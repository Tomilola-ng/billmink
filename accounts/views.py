from bills.models import Bill
from django.urls import reverse
from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from accounts.models import Profile, Withdraw
from django.views.generic import UpdateView, CreateView
from django.contrib.auth.decorators import login_required
from accounts.forms import UserAdminCreationForm, ProfileForm
from django.contrib.auth import logout, authenticate, login as login_func
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

"""
    Basic Views
"""

def index(req):
    if req.user.is_authenticated:
        bills = Bill.objects.filter(user = req.user)
        context = {
            'bills': bills
        }
        return render(req, 'dashboard/dashboard.html', context)
    return render(req, 'core/index.html')

def about(req):
    return render(req, 'core/about.html')
 
def agreement(req):
    return render(req, 'core/agreement.html')

"""
    Auth Views
"""

def register(req):
    form = UserAdminCreationForm()
    form_2 = ProfileForm()

    context = {
        'form' : form,
        'form_2' : form_2
    }

    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        form_2 = ProfileForm(req.POST)

        if form.is_valid() and form_2.is_valid():
            user = form.save()
            profile = form_2.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('signup_done_view')
        else:
            return render(req, 'auth/register.html', context )
    return render(req, 'auth/register.html', context )

"""
    Custom Views
"""

def page_not_found(req, exception):
   return render (req, 'core/404.html')

def wait(req):
    return render(req, 'withdraw/wait.html')

def signup_done(req):
    return render(req, 'auth/register_done.html')

"""
    Custom Views : Classes
"""

class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Profile
    template_name = 'accounts/form.html'
    fields = ['fullname', 'socialmedia']

    def form_valid(self, form):
        form.instance.user = self.request.user
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
        context['formname'] = 'Profile Update'
        context['multipart'] = True
        return context 
             

class WithdrawForm(LoginRequiredMixin, CreateView):
    model = Withdraw
    template_name = 'withdraw/form.html'
    fields = ['amount', 'account_number', 'account_name', 'bank_name']
    
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('wait_view')
    
    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['balance'] = self.request.user.profile.account_balance
        return context 
    