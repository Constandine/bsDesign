from django.contrib import admin
from websearch.models import Like
from websearch.models import Message
from websearch.models import Userprofile

admin.site.register(Userprofile)
admin.site.register(Like)
admin.site.register(Message)