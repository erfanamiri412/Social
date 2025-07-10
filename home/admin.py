from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# admin.site.register(Post)

#"""COSTUMISING ADMIN PANEL"""

# 1)
    # class PostAdmin(admin.ModelAdmin):
    #     list_display = ('user', 'slug', 'updated')
    #     search_fields = ('slug', 'body')
    #     list_filter = ('updated')
    #     prepopulated_fields = {'slug': ('body',)}
    #     raw_id_fields = ('user',)

    # admin.site.register(Post, PostAdmin)

# 2)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'updated')
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created', 'is_replay')
    raw_id_fields = ('user', 'post', 'reply')