from django.urls import path
from .views import bill_create, bill_update, bill_delete, bill_pay, update_bill
from accounts.views import activity
urlpatterns = [
    path('create/', bill_create.as_view(), name='bill_create_view'),
    path('accounts/', activity, name='activity_view'),
    path('<str:pk>/update/', bill_update.as_view(), name='bill_update_view'),
    path('<str:pk>/delete/', bill_delete.as_view(), name='bill_delete_view'),
    path('<uuid:id>/payment/', bill_pay, name='billPayment_view'),
    path('update/', update_bill, name='update_bill'),
    path('<uuid:id>/status/', bill_pay, name='payment_success'),
]