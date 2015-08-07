from django.shortcuts import render

# Create your views here.
# Settings for file uploads
from filehandler.models import UserFile, UserFileForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def list(request):
    # Handle file upload

    if request.method == 'POST':

        form = UserFileForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            new_user_file = UserFile(file = request.FILES['file'], user = request.user)
            new_user_file.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('filehandler.views.list'))
    else:

        form = UserFileForm() # A empty, unbound form

    # Load documents for the list page
    user_files = UserFile.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'user_files': user_files, 'form': form},
        context_instance=RequestContext(request)
    )
