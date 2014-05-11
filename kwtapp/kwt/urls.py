from django.conf.urls import patterns, include, url
from django.conf import settings
#~ from django.conf.urls import *
#~ import django.views.generic.simple.redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'kwt.views.grid', name='grid'),
    #~ url(r'^grid/$', 'kwt.views.grid', name='grif.html'),
    url(r'^home/$', 'kwt.views.home', name='home'),
    url(r'^manykw$', 'kwt.views.manykw', name='manykw'),
    url(r'^kw_db/$', 'kwt.views.kw_db', name='kw_db'),
    url(r'^kw_english/(?P<kw_english>[-\w]+)/$', 'kwt.views.kw_db1', name='kw_db1'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
