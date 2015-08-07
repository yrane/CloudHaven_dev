#!/usr/bin/env python
#-*- coding: utf-8 -*-

from Crypto import Random
from Crypto.Cipher import AES
from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect
from dropbox.client import DropboxOAuth2Flow
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from .models import UserConnection
from pydrive.auth import GoogleAuth
from oauth2client.client import OAuth2WebServerFlow
import json
import dropbox_functions
import google_functions
import box_functions
from pprint import pprint
from filehandler.models import UserFile, UserFileForm, UserFileChunks
import cStringIO, os, random, re, sys
import zfec
import cnox


key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
#Box modules
from boxsdk import OAuth2

# from google API console - convert private key to base64 or load from file
# id = "303238530248-g2sshp334fkmq3htovp6a0sps9p4tgmd@developer.gserviceaccount.com"
# key = 'mfyXhE4v_0lEConh4FcAJUjW'



client_id = "813087485002-lkn4dilg4355de3qu8g62ml3f2pe0pr1.apps.googleusercontent.com"
client_secret = "3d-QjtT9T-t0rb1FJ3_oAptu"
# redirect = "http://127.0.0.1:8000/"
scope = 'https://www.googleapis.com/auth/drive'
redirect_drive = "https://cloudhaven.mybluemix.net/drive-callback"
flow = OAuth2WebServerFlow(client_id=client_id,client_secret=client_secret,
                                scope=scope, redirect_uri=redirect_drive)

oauth = OAuth2(
    client_id='tdjl2abwsprtfcoc3e497zc8c3fnhwnf',
    client_secret='qjThWvl9J1VPbFlfC3MjXSeiIrF30yZ6',
    )

def drive_auth(request):
    gauth = GoogleAuth()

    authorize_url = flow.step1_get_authorize_url()

    return HttpResponseRedirect(authorize_url)

def drive_callback(request):
    query_params = request.GET
    credentials = flow.step2_exchange(request.REQUEST)
    try:
        info = request.user.connections.get(provider='gdrive-oauth2')
        info.credentials = credentials.to_json()
        info.save()
    except ObjectDoesNotExist:
        info = UserConnection(user=request.user, provider = "gdrive-oauth2", credentials = credentials.to_json())
        info.save()

    return redirect("/home")


def box_auth(request):


    auth_url, csrf_token = oauth.get_authorization_url('https://cloudhaven.mybluemix.net/box-callback')

    return HttpResponseRedirect(auth_url)

def box_callback(request):
    query_params = request.GET
    access_token, refresh_token = oauth.authenticate(query_params['code'])

    try:
        info = request.user.connections.get(provider='box-oauth2')

        creds = {}
        creds['access_token'] = access_token
        creds['refresh_token'] = refresh_token
        info.credentials = creds
        info.save()
    except ObjectDoesNotExist:
        creds = {}
        creds['access_token'] = access_token
        creds['refresh_token'] = refresh_token
        info = UserConnection(user=request.user, provider = "box-oauth2", credentials = json.dumps(creds))
        info.save()

    # redirect_uri = "http://127.0.0.1:8000/home"
    return redirect("/home")

    # pprint(vars(request))

@login_required(login_url='/account/login/')
def gethome(request):
    return render(request, 'index.html')

def get_dropbox_auth_flow(web_app_session):
    redirect_uri = "https://cloudhaven.mybluemix.net/dropbox-auth-finish"

    # return DropboxOAuth2Flow('5pj88hw5yji0813', '792vvk8g6un5lvc', redirect_uri,
    #                          web_apbox-auth-csrf-token")
    return DropboxOAuth2Flow('5pj88hw5yji0813', '792vvk8g6un5lvc', redirect_uri,
                             web_app_session, "dropbox-auth-csrf-token")

# URL handler for /dropbox-auth-start
def dropbox_auth_start( request):
    authorize_url = get_dropbox_auth_flow(request.session).start()
    return redirect(authorize_url)

# URL handler for /dropbox-auth-finish
def dropbox_auth_finish(request):

    query_params = request.GET

    try:
        pprint(vars(request.session))
        db_access_token, user_id, url_state  = get_dropbox_auth_flow(request.session).finish(query_params)
        creds = {}
        creds['access_token'] = db_access_token


        try:
            info = request.user.connections.get(provider='dropbox-oauth2')
            info.credentials = creds
            info.save()
            # TODO - You always get a new access token !!! Why? Is something wrong?
        except ObjectDoesNotExist:
            creds['uid'] = user_id
            info = UserConnection(user=request.user, provider = "dropbox-oauth2", credentials = json.dumps(creds))
            info.save()

    except DropboxOAuth2Flow.BadRequestException, e:
        http_status(400)
    except DropboxOAuth2Flow.BadStateException, e:
        # Start the auth flow again.
        redirect_to("/dropbox-auth-start")
    except DropboxOAuth2Flow.CsrfException, e:
        http_status(403)
    except DropboxOAuth2Flow.NotApprovedException, e:
        #flash('Not approved?  Why not?')
        #return redirect_to("/home")
        return redirect("/home")
        # redirect_to("/dropbox-auth-start")
    except DropboxOAuth2Flow.ProviderException, e:
        #logger.log("Auth error: %s" % (e,))
        http_status(403)

    redirect_uri = "/home"
    return redirect(redirect_uri)

def download_files(request):
    if request.method == 'POST':
        for key, value in request.POST.items():

            if re.match('file_+', key):
                file_to_download = UserFile.objects.get(name=value)

                file_chunks = UserFileChunks.objects.filter(file_id_id=file_to_download)

                directory = 'zfec_chunks'
                if not os.path.exists(directory):
                    os.makedirs(directory)

                ## Box commented to check whether rejoining works properly
                # box_functions.download_file(request, file_chunks, directory)
                dropbox_functions.download_file(request, file_chunks, directory)
                google_functions.download_file(request, file_chunks, directory)


                join_chunks(value)
                decrypt_files(value)
    redirect_uri = "/home"
    return redirect(redirect_uri)

def upload_files(request):
    if request.method == 'POST':
        form = UserFileForm(request.POST, request.FILES)
        if form.is_valid():

            uploaded_file = request.FILES['file']
            # upload_to_blobstore(uploaded_file)

            # download_from_blobstore()
            encrypted_file = encrypt_files(key, uploaded_file)

            # make_chunks(uploaded_file)
            make_chunks(encrypted_file)

            chunks = []

            # print chunks
            # sys.exit()
            uploaded_file_name = uploaded_file.name

            to_upload = "zfec_chunks/" + encrypted_file + "_chunk"
            # chunks.append(open(to_upload+".0_3.fec.enc",'rb'))
            # chunks.append(open(to_upload+".1_3.fec.enc",'rb'))
            # chunks.append(open(to_upload+".2_3.fec.enc",'rb'))
            chunks.append(open(to_upload+".0_3.fec",'rb'))
            chunks.append(open(to_upload+".1_3.fec",'rb'))
            chunks.append(open(to_upload+".2_3.fec",'rb'))

            new_user_file = None


            existing_file = UserFile.objects.filter(name=uploaded_file_name)
            if not existing_file:
                new_user_file = UserFile(user = request.user, name =  uploaded_file_name)
                new_user_file.save()

            #check if user connections exists for each service before uploading
            # box_functions.upload_file(request,existing_file, new_user_file, uploaded_file)
            # dropbox_functions.upload_file(request,existing_file, new_user_file, uploaded_file)
            # google_functions.upload_file(request,existing_file, new_user_file, uploaded_file)
            box_functions.upload_file(request,existing_file, new_user_file, chunks[0])
            dropbox_functions.upload_file(request,existing_file, new_user_file, chunks[1])
            google_functions.upload_file(request,existing_file, new_user_file, chunks[2])



    filelist = [ f for f in os.listdir("zfec_chunks")]

    for f in filelist:
        os.remove(os.path.join("zfec_chunks", f))

    redirect_uri = "/home"
    return redirect(redirect_uri)


def make_chunks(uploaded_file):

    # PREFIX = uploaded_file.name + "_chunk"
    # SUFFIX = ".fec"
    # VERBOSE=False
    #
    # tempdir = 'zfec_chunks'
    # if not os.path.exists(tempdir):
    #     os.makedirs(tempdir)
    # try:
    #     tempf = file(os.path.join(tempdir, uploaded_file.name), 'w+b')
    #     fsize = len(uploaded_file.file.read())
    #     uploaded_file.file.seek(0)
    #     tempf.write(uploaded_file.file.read())
    #     tempf.flush()
    #     tempf.seek(0)
    #     k = 2
    #     m = 3
    #     # encode the file
    #     chunks = zfec.filefec.encode_to_files(tempf, fsize, tempdir, PREFIX, k, m, SUFFIX, verbose=VERBOSE)
    #     print chunks.__class__
    #     print "\n" + str(len(chunks))
    #     # print len(chunks[0])
    #     print "------------------"
    #     # print chunks
    #     print chunks[0]
    # finally:
    #     print "done encoding"
    #
    PREFIX = uploaded_file + "_chunk"
    SUFFIX = ".fec"
    VERBOSE=False

    tempdir = 'zfec_chunks'
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)
    try:
        tempf = open(os.path.join(tempdir, uploaded_file), 'rb')
        # tempf = file(os.path.join(tempdir, uploaded_file), 'w+b')
        fsize = len(tempf.read())
        # uploaded_file.file.seek(0)
        # tempf.write(uploaded_file.file.read())
        tempf.flush()
        tempf.seek(0)
        k = 2
        m = 3
        # encode the file
        zfec.filefec.encode_to_files(tempf, fsize, tempdir, PREFIX, k, m, SUFFIX, verbose=VERBOSE)
        # print chunks.__class__
        # print "\n" + str(len(chunks))
        # # print len(chunks[0])
        # print "------------------"
        # # print chunks
        # print chunks[0]
    finally:
        print "done encoding"


def join_chunks(file_name):
    PREFIX = file_name + ".nox_chunk"
    SUFFIX = ".fec"
    VERBOSE=False
    numshs = None
    tempdir = 'zfec_chunks'

    # select some share files
    RE=re.compile(zfec.filefec.RE_FORMAT % (PREFIX, SUFFIX,))
    fns = os.listdir(tempdir)
    # print fns
            # assert len(fns) >= m, (fns, tempdir, tempdir,)
    # sharefs = [ open(os.path.join(tempdir, fn), "rb") for fn in fns if RE.match(fn) ]
    sharefs = [open(os.path.join(tempdir, fn),"rb") for fn in fns]
    # random.shuffle(sharefs)
    print sharefs
    # del sharefs[numshs:]

    download_dir = 'Downloads'
    if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

    outfile = file_name + ".nox"
    outf = file(os.path.join(download_dir, outfile), 'w+b')


    zfec.filefec.decode_from_files(outf, sharefs, verbose=VERBOSE)
    outf.flush()
    outf.seek(0)

    # filelist = [ f for f in os.listdir("Downloads")]

    for f in sharefs:
        # if re.match("*fec", f):
        os.remove(f.name)


def encrypt_files(key, uploaded_file):

    tempdir = 'zfec_chunks'
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)

    tempf = file(os.path.join(tempdir, uploaded_file.name), 'w+b')
    uploaded_file.file.seek(0)
    tempf.write(uploaded_file.file.read())
    tempf.flush()
    tempf.seek(0)

    to_upload = "zfec_chunks/" + uploaded_file.name
    # file1 = open(to_upload,'rb')
    # file2 = open(to_upload+".1_3.fec",'rb')
    # file3 = open(to_upload+".2_3.fec",'rb')


    cnox.Encrypt(in_file=to_upload, key=key)

    # plaintext = file1.read()
    # enc = encrypt(plaintext, key)
    #
    #
    # with open(to_upload + ".enc", 'wb') as fo:
    #     fo.write(enc)

    # os.remove(to_upload)
    encrypted_file = uploaded_file.name + ".nox"
    return encrypted_file
    # plaintext = file2.read()
    # enc = encrypt(plaintext, key)

    # file_name =to_upload+".1_3.fec"
    # with open(file_name + ".enc", 'wb') as fo:
    #     fo.write(enc)
    #
    # plaintext = file3.read()
    # enc = encrypt(plaintext, key)
    #
    # file_name =to_upload+".2_3.fec"
    # with open(file_name + ".enc", 'wb') as fo:
    #     fo.write(enc)


    # with open(file_name, 'rb') as fo:
    #     plaintext = fo.read()
    # enc = encrypt(plaintext, key)

    # name = file_name + ".enc"
    # return name

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")


def decrypt_files(file_name):
    # PREFIX = file_name + ".enc"
    # SUFFIX = ".fec.enc"
    #
    # tempdir = 'Downloads'
    # # select some share files
    # RE=re.compile(zfec.filefec.RE_FORMAT % (PREFIX, SUFFIX,))
    #
    # fns = os.listdir(tempdir)
    #
    #         # assert len(fns) >= m, (fns, tempdir, tempdir,)
    # sharefs = [ os.path.join(tempdir, fn) for fn in fns if RE.match(fn) ]
    # print sharefs
    # for f in sharefs:
    f = file_name + ".nox"
    tempdir = 'Downloads'

    file_path = os.path.join(tempdir, f)
    cnox.Decrypt(in_file=file_path,key=key)
    # fo = open(os.path.join(tempdir, f), 'rb')
    # ciphertext = fo.read()
    # dec = decrypt(ciphertext, key)
    # with open(os.path.join(tempdir, f[:-4]), 'wb') as fo:
    #     fo.write(dec)

    os.remove(os.path.join(tempdir, f))
    # for f in sharefs:
    #     # if re.match("*fec", f):
    #     os.remove(f)

    # with open(file_name, 'rb') as fo:
    #     ciphertext = fo.read()
    #
    # dec = decrypt(ciphertext, key)
    #
    # #with open(file_name[:-4], 'wb') as fo:
    # with open(file_name[:-4], 'wb') as fo:
    #     fo.write(dec)


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=256):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

# def upload_to_blobstore(to_upload):
#     upload_files = blobstore_handlers.BlobstoreUploadHandler.get_uploads('file')
#     blob_info = upload_files[0]
#     blobstore_handlers.BlobstoreUploadHandler.redirect('/home')
#
# def download_from_blobstore():
#     for b in blobstore.BlobInfo.all():
#         if not blobstore.get(b.key()):
#             blobstore_handlers.BlobstoreDownloadHandler.error(404)
#         else:
#             blobstore_handlers.BlobstoreDownloadHandler.send_blob(blobstore.BlobInfo.get(b.key()), save_as=True)
