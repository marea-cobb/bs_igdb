from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import bs_igdbview.views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    # Sends requests to filter functions
    url(r'^search/result', 'bs_igdbview.views.result_filter'),
    url(r'^search/junction', 'bs_igdbview.views.junction_filter'),
    url(r'^search/summary', 'bs_igdbview.views.summary_filter'),
    url(r'^search/sequence', 'bs_igdbview.views.sequence_filter'),
    url(r'^search/alignment2', 'bs_igdbview.views.alignment_filter2'),
    url(r'^full_search/results', 'bs_igdbview.views.full_search_filter'),


    # Basic Table Views:
    url(r'^result', 'bs_igdbview.views.result'),
    url(r'^junction', 'bs_igdbview.views.junction'),
    url(r'^summary', 'bs_igdbview.views.summary'),
    url(r'^sequence', 'bs_igdbview.views.sequence'),
    url(r'^alignment', 'bs_igdbview.views.alignment'),
    url(r'^full_search', 'bs_igdbview.views.full_search'),



    #Home page urls
    url(r'^$', bs_igdbview.views.dashboard),
    # url(r'^$', bs_igdbview.views.dashboard),

    # Admin view and admin documentation
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # url(r'^admin/', include(templates.admin))


)
