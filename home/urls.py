from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url('^$', TemplateView.as_view(template_name='landing.html')),

    # TODO - The view gethome was added so that one can access this page only when logged in. Check if all good again
    #url('^home', TemplateView.as_view(template_name='index.html')),
    url('^home', 'home.views.gethome'),

    url(r'^dropbox_auth', 'home.views.dropbox_auth_start', name='dropbox_auth'),
    url(r'^drive_auth', 'home.views.drive_auth', name='drive_auth'),
    url(r'^box_auth', 'home.views.box_auth', name='box_auth'),
    url(r'^dropbox-auth-finish', 'home.views.dropbox_auth_finish', name='dropbox-auth-finish'),
    url(r'^drive-callback', 'home.views.drive_callback', name='drive-callback'),
    url(r'^box-callback', 'home.views.box_callback', name='box-callback'),

    url(r'^upload_files', 'home.views.upload_files', name='upload_files'),
    url(r'^download_files', 'home.views.download_files', name='download_files'),
)