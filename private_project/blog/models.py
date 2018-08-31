from django.db import models
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpendMethod, ReadNumDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpendMethod):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    read_num = GenericRelation(ReadNumDetail)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog: {}>'.format(self.title)

    class Meta:
        ordering = ['-create_time']
