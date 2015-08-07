from filehandler.models import UserFile, UserFileForm

def user_dropbox_connection(request):
    if hasattr(request.user, 'connections'):
        user_dropbox_connection_obj = request.user.connections.filter(provider = "dropbox-oauth2")
        if( user_dropbox_connection):
            return {'user_dropbox_connection': user_dropbox_connection_obj}
    else:
        return {'user_dropbox_connection': None }

def user_google_connection(request):
    if hasattr(request.user, 'connections'):
        user_google_connection_obj = request.user.connections.filter(provider = "gdrive-oauth2")
        if( user_google_connection):
            return {'user_google_connection': user_google_connection_obj}
    else:
        return {'user_google_connection': None }

def user_box_connection(request):
    if hasattr(request.user, 'connections'):
        user_box_connection_obj = request.user.connections.filter(provider = "box-oauth2")
        if(user_box_connection):
            return {'user_box_connection': user_box_connection_obj}
    else:
        return {'user_box_connection': None }


def user_files_uploaded(request):
    if hasattr(request.user, 'files'):
        user_files_obj = request.user.files.all()
        if( len(user_files_obj) > 0):
            return {'user_files': user_files_obj}
        else:
            return {'user_files': None}
    else:
        return {'user_files': None }

def user_file_upload_form(request):
    form = UserFileForm()
    return {'fileuploadform': form}