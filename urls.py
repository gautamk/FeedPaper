from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from FeedPaper import FP
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
)
