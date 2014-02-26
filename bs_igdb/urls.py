from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import bs_igdbview.views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    # Sends requests to filter functions
    url(r'^bs_igdb/search/result', 'bs_igdbview.views.result_filter'),
    url(r'^bs_igdb/search/junction', 'bs_igdbview.views.junction_filter'),
    url(r'^bs_igdb/searh/summary', 'bs_igdbview.views.summary_filter'),
    url(r'^bs_igdb/search/sequence', 'bs_igdbview.views.sequence_filter'),
    url(r'^bs_igdb/search/alignment2', 'bs_igdbview.views.alignment_filter2'),
    url(r'^bs_igdb/full_search/results', 'bs_igdbview.views.full_search_filter'),


    # Basic Table Views:
    url(r'^bs_igdb/result', 'bs_igdbview.views.result'),
    url(r'^bs_igdb/junction', 'bs_igdbview.views.junction'),
    url(r'^bs_igdb/summary', 'bs_igdbview.views.summary'),
    url(r'^bs_igdb/sequence', 'bs_igdbview.views.sequence'),
    url(r'^bs_igdb/alignment', 'bs_igdbview.views.alignment'),
    url(r'^bs_igdb/full_search', 'bs_igdbview.views.full_search'),



    #Home page urls
    url(r'^bs_igdb/', bs_igdbview.views.dashboard),
    # url(r'^$', bs_igdbview.views.dashboard),

    # Admin view and admin documentation
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(templates.admin))


)
