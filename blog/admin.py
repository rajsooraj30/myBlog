from django.contrib import admin
from .models import Post, BlogComment


# Register your models here.

@admin.register(Post)
class PostModel(admin.ModelAdmin):
    list_display = ['sno', 'title', 'author', 'content', 'displayContent', 'slug', 'timestamp']

    class Media:
        js = ('tinyinject.js',)


@admin.register(BlogComment)
class BlogCommentModel(admin.ModelAdmin):
    list_display = ['sno', 'comment', 'user', 'post', 'parent', 'timestamp']
