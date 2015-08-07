from django.contrib import admin

# Register your models here.
from .models import UserConnection
from filehandler.models import UserFile
from filehandler.models import UserFileChunks
admin.site.register(UserConnection)
admin.site.register(UserFile)
admin.site.register(UserFileChunks)