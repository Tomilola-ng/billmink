from django.contrib import admin
from bills.models import Bill, Activity

# Register your models here.
admin.site.register(Bill)
admin.site.register(Activity)