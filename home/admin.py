from django.contrib import admin
from home.models import Friend, Post, BlogPost, Comment







# Register your models here.
admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(BlogPost)
admin.site.register(Comment)