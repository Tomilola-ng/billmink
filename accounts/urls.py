from django.urls import path
from .views import update_profile, WithdrawForm, wait, signup_done


urlpatterns = [
    path('profile/<int:pk>/update/', update_profile.as_view(), name='profile_update_view'),
    path('withdraw/', WithdrawForm.as_view(), name='withdraw_view'),
    path('wait/', wait, name = 'wait_view'),
    path('signup_done/', signup_done, name = 'signup_done_view'),
]