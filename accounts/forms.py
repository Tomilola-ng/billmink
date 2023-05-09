from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import Profile, Withdraw
from django.core.validators import URLValidator


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['phone']
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'socialmedia']

    socialmedia = forms.URLField(validators=[URLValidator()], required=True)        
