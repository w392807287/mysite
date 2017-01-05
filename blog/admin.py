from django.contrib import admin
from .models import Author, Article, Tag, Column, Category

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'reading_count', 'pub_date')
    list_filter = ('author', 'category', 'reading_count', 'pub_date', 'column')
    search_fields = ('title', 'author', 'category', 'summary', 'content')


admin.site.register(Author)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Column)
admin.site.register(Category)
admin.site.register(Tag)
