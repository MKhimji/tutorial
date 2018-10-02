from django.contrib import admin
from home.models import BlogPost, Like
from django.db import models
from ckeditor.widgets import CKEditorWidget


#class BlogAdmin(admin.ModelAdmin):
    #formfield_overrides = {
     #   models.TextField: {'widget': CKEditorWidget()},
    #}




# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Like)