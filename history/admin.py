from django.contrib import admin

from .models import ReadHistory
# Register your models here.

@admin.register(ReadHistory)
class ReadHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content_object', 'last_read_time']
