from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'IFDB.views.home', name='home'),
    # url(r'^IFDB/', include('IFDB.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^imdb/', include('imdb.urls')),
    url(r'^movies/', include('movies.urls')),
    url(r'^bom/', include('boxofficemojo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
