from django.contrib import admin
from .models import Book, NewBook, RecommendBook


admin.site.register(Book)
admin.site.register(NewBook)
admin.site.register(RecommendBook)
