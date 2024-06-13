from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from _data import herobizds


template_name = herobizds.context['template_name']


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            template_name + ':home',
        ]

    def location(self, item):
        return reverse(item)
