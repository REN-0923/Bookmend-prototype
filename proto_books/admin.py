from django.contrib import admin

# Register your models here.

from .models import BookmarkModel

admin.site.register(BookmarkModel)