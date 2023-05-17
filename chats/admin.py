from django.contrib import admin

from .models import *

admin.site.register(Thread)
admin.site.register(ThreadComment)
admin.site.register(ThreadReply)
admin.site.register(ReThread)
admin.site.register(ThreadImage)

admin.site.register(ThreadLike)


