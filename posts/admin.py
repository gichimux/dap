from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(RePost)
admin.site.register(PostImage)

admin.site.register(Like)


