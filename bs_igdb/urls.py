from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'igdb.views.home', name='home'),
    url(r'^bs_igdb/', include('bs_igdbview.urls')),
    # url(r'^admin/', include(templates.admin))

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # admin.autodiscover()
)
