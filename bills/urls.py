from django.urls import path
from .views import billCreate, billUpdate, billDelete, bill_pay, activity, update_bill

urlpatterns = [
    path('create/', billCreate.as_view(), name='billCreate_view'),
    path('accounts/', activity, name='activity_view'),
    path('<str:pk>/update/', billUpdate.as_view(), name='billUpdate_view'),
    path('<str:pk>/delete/', billDelete.as_view(), name='billDelete_view'),
    path('<uuid:id>/payment/', bill_pay, name='billPayment_view'),
    path('update/', update_bill, name='update_bill'),
    path('<uuid:id>/status/', bill_pay, name='payment_success'),
]