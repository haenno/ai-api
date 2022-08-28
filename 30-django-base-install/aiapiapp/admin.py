from django.contrib import admin

# Register your models here.
from aiapiapp.models import ChatUuid, ChatDialogue
admin.site.register(ChatUuid)
admin.site.register(ChatDialogue)
