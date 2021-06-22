from django.contrib import admin
from .models import Post, Comment, Attachment


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Attachment)
