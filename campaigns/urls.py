from django.urls import path
from campaigns.views import campaign_create, campaign_update, campaign_list, campaign_update_image, campaign_donate

urlpatterns = [
    path('', campaign_list.as_view(), name="campaign_list_view"),
    path('create/', campaign_create.as_view(), name='campaign_create_view'),
    path('update/<slug:slug>/', campaign_update.as_view(), name='campaign_update_view'),
    path('update/image/<slug:slug>/', campaign_update_image.as_view(), name='campaign_update_image_view'),
    path('donate/<slug:slug>/', campaign_donate, name='campaign_donate_view'),
]