from django.contrib import admin

from library.models import BookLog, Book

# Register your models here.
admin.site.register(Book)
admin.site.register(BookLog)