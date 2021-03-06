from django.contrib import admin
from .models import ReadNum, ReadNumDetail
# Register your models here.


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = [
        'read_num',
    ]


@admin.register(ReadNumDetail)
class ReadNumDetailAdmin(admin.ModelAdmin):
    list_display = [
        'read_num',
        'date',
    ]