from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('websearch.urls', namespace="websearch")),
    url(r'^websearch/', include('websearch.urls', namespace="websearch")),
    # Examples:
    # url(r'^$', 'bsDesign.views.home', name='home'),
    # url(r'^bsDesign/', include('bsDesign.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/Users/apple/Desktop/xiumu/Study/bsDesign/static'}
    ),
)
