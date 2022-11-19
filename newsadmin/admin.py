from django.contrib import admin
from .models import *


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('id','source', 'date_added')

admin.site.register(NewsItem,NewsItemAdmin)
admin.site.register(StoredNewsItem)
