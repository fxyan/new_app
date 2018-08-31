from django.contrib import admin
from .models import BlogType, Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'content',
        'blog_type',
        'get_read_num',
        'create_time',
        'last_update_time',
    ]


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = [
        'type_name',
    ]
