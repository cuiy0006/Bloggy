from django.contrib import admin
from comments.models import Comment, CommentExtension

# Register your models here.
admin.site.register(Comment)
admin.site.register(CommentExtension)
