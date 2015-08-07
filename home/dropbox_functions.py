from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import json
import dropbox
from filehandler.models import UserFileChunks
from pprint import pprint
import os, ntpath


def authenticate(request):
    user_instance = request.user.connections.get(provider='dropbox-oauth2')
    acc_token = json.loads(user_instance.credentials)['access_token']
    client = dropbox.client.DropboxClient(acc_token)

    return client

def download_file(request, file_chunks, directory):
    dropbox_chunk = file_chunks.get(service="dropbox")
    dropbox_file_name = dropbox_chunk.name
    ## Download from Dropbox
    client = authenticate(request)
    f,metadata = client.get_file_and_metadata(dropbox_file_name)
    filepath = os.path.join(directory, dropbox_file_name)
    out = open(filepath, 'wb')
    out.write(f.read())
    out.close()


def upload_file(request,existing_file, new_user_file, uploaded_file):
    uploaded_file_name = uploaded_file.name
    # file_dropbox = uploaded_file.file
    head, tail = ntpath.split(uploaded_file_name)
    uploaded_file_name = tail

    file_dropbox = uploaded_file

    file_dropbox.seek(0)


    try:
        client = authenticate(request)
        file1 = client.put_file(uploaded_file_name, file_dropbox.read(), overwrite=True)
        # TODO - Only saving the file name right now. Will be used for Reed Solomon chunk later

        if not existing_file:
            file_chunk = UserFileChunks(file_id = new_user_file,identifier = file1["rev"], name = uploaded_file_name, service="dropbox")
            file_chunk.save()
    except ObjectDoesNotExist:
        #print "DropBox not linked yet!"
        redirect_uri = "/home"
        return redirect(redirect_uri)
    except dropbox.rest.ErrorResponse, e:
        print "DropBox not linked yet!"
        # redirect_uri = "http://127.0.0.1:8000/home"
        # return redirect(redirect_uri)
        return redirect("/dropbox_auth")
