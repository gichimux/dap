from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Repost)
admin.site.register(Like)


