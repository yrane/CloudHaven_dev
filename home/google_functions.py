#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.client import Credentials
from filehandler.models import UserFile, UserFileChunks
import os, ntpath
from pprint import pprint
import sys


def authenticate(request):
    user_instance = request.user.connections.get(provider='gdrive-oauth2')

    cred = Credentials.new_from_json(user_instance.credentials)
    gauth = GoogleAuth()
    gauth.credentials = cred
    if gauth.access_token_expired:
    # Refresh them if expired

        print "refreshing"
        gauth.Refresh()
        try:
            info = request.user.connections.get(provider='gdrive-oauth2')
            info.credentials = gauth.credentials.to_json()
            info.save()
        except ObjectDoesNotExist:
            info = UserConnection(user=request.user, provider = "gdrive-oauth2", credentials = gauth.credentials.to_json())
            info.save()

        # pprint(vars(creds))

    else:
    # Initialize the saved creds
        gauth.Authorize()

    service = GoogleDrive(gauth)

    return service

def download_file(request, file_chunks, directory):
##Download from google drive
    chunk = file_chunks.get(service="gdrive")
    service = authenticate(request)
    file_object = service.CreateFile({'id': chunk.identifier})

    filepath = os.path.join(directory, chunk.name)
    file_object.GetContentFile(filepath)


def upload_file(request,existing_file, new_user_file, uploaded_file):

    uploaded_file_name = uploaded_file.name
    # file_drive = uploaded_file.file
    head, tail = ntpath.split(uploaded_file_name)
    uploaded_file_name = tail

    file_drive = uploaded_file

    try:
        drive_service = authenticate(request)
        file_list = drive_service.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

        exists = False
        for file1 in file_list:
            if file1['title'] == "CloudHaven":
                exists = True
                folder = {}
                folder['id'] = file1['id']
                break

        if exists == False:
            folder = drive_service.CreateFile({'title': 'CloudHaven', "mimeType": "application/vnd.google-apps.folder"})
            folder.Upload()

        if not existing_file:
            file_upload = drive_service.CreateFile({'title':uploaded_file_name, #'mimeType':uploaded_file.content_type,
                "parents": [{"kind": "drive#fileLink","id": folder['id']}]})
            print file_drive
            # file_upload.SetContentString(file_drive.read())
            file_upload.SetContentString(file_drive.read().decode(sys.getdefaultencoding()).encode('utf-8'))
            file_upload.Upload() # Files.insert()
            file_chunk = UserFileChunks(file_id = new_user_file, identifier=file_upload['id'], name = file_upload['title'], service="gdrive")
            file_chunk.save()
        else:
            existing_file = UserFile.objects.get(name=uploaded_file_name)
            existing_chunk = existing_file.chunks.get(service="gdrive")
            file_upload = drive_service.CreateFile({'id': existing_chunk.identifier})

            # file_upload.SetContentString(file_drive.read())
            file_upload.SetContentString(file_drive.read().decode(sys.getdefaultencoding()).encode('utf-8'))

            # file_upload.SetContentString(unicode(file_drive.read(), 'utf-8'))
            file_upload.Upload() # Files.insert()
            existing_chunk.identifier = file_upload['id']
            existing_chunk.save()
    except ObjectDoesNotExist:
        print "Google Drive not linked yet!"
        redirect_uri = "/home"
        return redirect(redirect_uri)
