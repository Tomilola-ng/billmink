import requests
from django.urls import reverse
from django.conf import settings
from bills.models import Activity
from django.contrib import messages
from django.conf import settings
from campaigns.models import Campaign
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

User = settings.AUTH_USER_MODEL



def campaign_detail(req, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    li_nk = f'http://{settings.DOMAIN_PATH}/{slug}'

    context = {
        'campaign' : campaign,
        'li_nk': li_nk
    }
    return render(req, 'campaigns/campaign_detail.html', context)



"""
    Class Views
"""



class campaign_list(ListView):
    model = Campaign
    context_object_name = 'campaigns'


class campaign_create(LoginRequiredMixin , CreateView):
    model = Campaign
    fields = ['name', 'donation_type', 'currency' ,'goal_amount', 'description', 'public']

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formname'] = 'Creating campaign page'
        return context 

    def form_valid(self, form):
        form.instance.user = self.request.user

        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f'Created a {form.instance.donation_type} campaign page'
        acc.save()
        
        return super().form_valid(form)
 
    def get_success_url(self):
        return reverse('campaign_update_image_view', args=[self.object.slug])
    

class campaign_update(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Campaign
    fields = ['name', 'description', 'donation_type', 'public']

    def form_valid(self, form):
        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f'Updated the { self.object } campaign'
        acc.save()

        return super().form_valid(form)

    def test_func(self):
        campaign = self.get_object()
        if self.request.user == campaign.user:
            return True
        return False

    def get_success_url(self):
        return reverse('index_view')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formname'] = 'Updating campaign page'
        return context 


class campaign_update_image(LoginRequiredMixin, UserPassesTestMixin , UpdateView):
    model = Campaign
    fields = ['image']
    template_name = 'campaigns/img_update.html'

    def form_valid(self, form):
        acc  = Activity.objects.create()
        acc.profile = self.request.user.profile
        acc.description = f'Updated the { self.object } campaign image'
        acc.save()

        return super().form_valid(form)

    def test_func(self):
        campaign = self.get_object()
        if self.request.user == campaign.user:
            return True
        return False

    def get_success_url(self):
        return reverse('index_view')

    def get_context_data(self, *args ,**kwargs):
        context = super().get_context_data(**kwargs)
        context['formname'] = 'Updating campaign page'
        context['img'] = self.object.image
        return context 
        


"""
    Related to Payments
"""



@login_required        
def campaign_donate(req, slug):
    campaign = get_object_or_404(Campaign, slug = slug)

    context = {
        'campaign': campaign,
        'account_balance': req.user.profile.account_balance
    }

    return render(req, 'campaigns/pay.html', context)

