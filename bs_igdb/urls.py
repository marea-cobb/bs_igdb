from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import bs_igdbview.views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^bs_igdb/result', 'bs_igdbview.views.result'),
    url(r'^bs_igdb/junction', 'bs_igdbview.views.junction'),
    url(r'^bs_igdb/summary', 'bs_igdbview.views.summary'),
    url(r'^bs_igdb/sequence', 'bs_igdbview.views.sequence'),
    url(r'^bs_igdb/alignment', 'bs_igdbview.views.alignment'),
    url(r'^bs_igdb/', bs_igdbview.views.dashboard),
    url(r'^$', bs_igdbview.views.dashboard),

    # url(r'^library/', bs_igdbview.views.ListLibraryView.as_view(), name='library-list',),
    # url(r'^admin/', include(templates.admin))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # admin.autodiscover()
)
