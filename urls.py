from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^UpdateItems/','FP.views.UpdateItems'),
    (r'^ShowUpdateItems/','FP.views.ShowUpdateItems'),
    (r'^UploadCSV/','FP.views.CSVUploadView'),
    
    # Example:
    # (r'^FeedPaper/', include('FeedPaper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls) ),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^/?','FP.views.LandingPage'),
)
