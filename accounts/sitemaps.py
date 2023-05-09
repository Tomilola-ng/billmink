from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index_view', 'agreement_view', 'about_view', 'register_view', 'login_view']
    def location(self, item):
        return reverse(item)