from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import bs_igdbview.views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bs_igdb.views.home', name='home'),
    url(r'^bs_igdb/result', 'bs_igdbview.views.result'),
    # url(r'^result/', 'bs_igdbview.views.result'),
    url(r'^bs_igdb/', bs_igdbview.views.dashboard),


    # url(r'^library/', bs_igdbview.views.ListLibraryView.as_view(), name='library-list',),
    # url(r'^admin/', include(templates.admin))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # admin.autodiscover()
)
