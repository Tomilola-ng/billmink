from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django .conf.urls.static import static

from accounts.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('auth/', admin.site.urls),
    path('', accounts_views.index, name='index_view'),

    # MISC
    path('about/', accounts_views.about, name='about_view'),
    path('agreement/', accounts_views.agreement, name='agreement_view'),

    # BILLS APP
    path('bill/', include('bills.urls')),

    # ACCOUNTS APP
    path('', include('accounts.urls')),

    # SITEMAPS
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Auth Views
    path('login/', auth_views.LoginView.as_view(template_name = 'auth/login.html'), name='login_view'),
    path('register/', accounts_views.register, name='register_view'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "accounts.views.page_not_found"