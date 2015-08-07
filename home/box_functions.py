
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import json
# from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import Credentials
from .models import UserConnection
from filehandler.models import UserFile, UserFileChunks
import os
from boxsdk import OAuth2, Client
import ntpath
def authenticate(request):
    user_instance = request.user.connections.get(provider='box-oauth2')

    acc_token = json.loads(user_instance.credentials)['access_token']
    refresh_token = json.loads(user_instance.credentials)['refresh_token']

    oauth = OAuth2(
    client_id='tdjl2abwsprtfcoc3e497zc8c3fnhwnf',
    client_secret='qjThWvl9J1VPbFlfC3MjXSeiIrF30yZ6',
    access_token=acc_token,
    refresh_token=refresh_token,
    )
    oauth.refresh(access_token_to_refresh=acc_token)
    creds = {}
    creds['access_token'] = oauth._access_token
    creds['refresh_token'] = oauth._refresh_token

    try:
        info = request.user.connections.get(provider='box-oauth2')
        info.credentials = json.dumps(creds)
        info.save()
    except ObjectDoesNotExist:
        info = UserConnection(user=request.user, provider = "box-oauth2", credentials = json.dumps(creds))
        info.save()
    # auth response = request.post()

    client = Client(oauth)
    # auth_url, csrf_token = oauth.get_authorization_url('/box-callback')

    # response = client.make_request('POST',auth_url)
    # print response
    # pprint(vars(response))
    return client

def download_file(request, file_chunks, directory):
##Download from Box
    chunk = file_chunks.get(service="box")
    service = authenticate(request)
    file_object = service.file(file_id=chunk.identifier)

    filepath = os.path.join(directory, chunk.name)
    file_write = open(filepath,'wb')
    file_object.download_to(file_write)


def upload_file(request,existing_file, new_user_file, uploaded_file):
    uploaded_file_name = uploaded_file.name
    print uploaded_file_name
    head, tail = ntpath.split(uploaded_file_name)
    uploaded_file_name = tail
    print uploaded_file_name
    # file_box = uploaded_file.file
    file_box = uploaded_file

    try:
        box_service = authenticate(request)

        root_folder = box_service.folder(folder_id='0').get()

        file_list = root_folder.get_items(limit=1000,offset=0)

        exists = False
        for file1 in file_list:
            if file1.name == "CloudHaven":

                exists = True
                folder = {}
                # folder = box_service.folder(file1.id)
                folder['id'] = file1.id
                cloud_folder = file1
                break

        if exists == False:

            cloud_folder = root_folder.create_subfolder('CloudHaven')
            folder = {}
                # folder = box_service.folder(file1.id)
            folder['id'] = cloud_folder.id

        if not existing_file:

            file_upload = cloud_folder.upload_stream(file_box, uploaded_file_name)
            file_chunk = UserFileChunks(file_id = new_user_file, identifier = file_upload.id,  name = file_upload.name, service="box")
            file_chunk.save()
        else:
            existing_file = UserFile.objects.get(name=uploaded_file_name)
            existing_chunk = existing_file.chunks.get(service="box")
            # file_id = existing_chunk.name
            file_object = box_service.file(file_id=existing_chunk.identifier)
            # file_upload = cloud_folder.upload_stream(file_box, uploaded_file_name)
            file_upload = file_object.update_contents_with_stream(file_box)

            existing_chunk.identifier = file_upload.object_id
            existing_chunk.save()
    except ObjectDoesNotExist:
        print "Box not linked yet!"
        redirect_uri = "/home"
        return redirect(redirect_uri)
