from django.urls import path
from .views import UpdateProfile, WithdrawForm, wait, signup_done


urlpatterns = [
    path('<int:pk>/update/', UpdateProfile.as_view(), name='profileUpdate_view'),
    path('withdraw/', WithdrawForm.as_view(), name='withdraw_view'),
    path('wait/', wait, name = 'wait_view'),
    path('signup_done/', signup_done, name = 'signup_done_view'),
]