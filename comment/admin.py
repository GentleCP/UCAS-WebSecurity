from django.contrib import admin

from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object','comment_content','comment_user','comment_time')
