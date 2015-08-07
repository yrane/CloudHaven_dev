from django.conf.urls import patterns, include, url
from django.contrib import admin

# For file uploads
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CloudHaven.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('allauth.urls')),
    url(r"^account/", include("account.urls")),
    url(r'', include('home.urls')),
    url(r'', include('filehandler.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# TODO - The last line only works for development mode. DANGEROUS for PRODUCTION
