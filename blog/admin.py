from django.contrib import admin
from .models import Author, Article, Tag, Column, Category

# Register your models here.
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Column)
admin.site.register(Category)
admin.site.register(Tag)
