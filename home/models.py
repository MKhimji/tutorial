from django.db import models
from django.contrib.auth.models import User
from django import forms
from django_extensions.db.fields import AutoSlugField
from tinymce.models import HTMLField


# Create your models here.

##We can have the user GET the empty form on the home page, allow the user to
##type something in there and then send a POST request to the web server
##What we need the model is for is to associate the POST request to the webserver
##with a logged in user.

##post is the text the user enters
##user is just relating the particular post to the user ('User') is imported



class Post(models.Model):
    post = models.CharField(max_length=500)
    user = models.ForeignKey(User)
##auto_now_add will date the object on creation but not on subsequent saves
    created = models.DateTimeField(auto_now_add=True) 
##allows users to edit their posts, will update the date to the date of edit
    updated = models.DateTimeField(auto_now_add=True)

##Need a way of checking  whether the friend object were trying to get already has the current user as the owner of the friends list
##So need to specifiy current_user in the Friend model
##related_name is django thing

##one object in this Friend model defines the relationship between the logged in users and other users on the website.
class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name = 'owner', null=True)

##current_user and new_friend are 2 user instances, current_user is logged in user

##create a Friend instance(friend) i.e an object of 2 users linked together
## and created returns a boolean value of whether the Friend object instance,i.e. friend was created or not
##get or create gets an object from the database or creates one if there isnt already a reliationship
##current_user = current_user is an if statement
    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user

        )
        friend.users.add(new_friend)


    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user

        )
        friend.users.remove(new_friend)


class BlogPost(models.Model):
    pic = models.ImageField(upload_to= 'profile_image', blank=True)
    title = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = HTMLField()
    slug = AutoSlugField(null=True, default=None,overwrite=True, unique=True, populate_from='title')

#added overwrite = True because after i changed the title of the blogpost in admin it didnt update the slug and reused the old title



    def __str__(self):
        return "%s %s %s %s " %(self.title, self.author.username, self.author.first_name, self.author.last_name)


class Comment(models.Model):
    Name = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    comment_body = models.ForeignKey(BlogPost)
    comment = models.CharField(max_length=500)

    def __str__(self):
        return "%s %s" %(self.Name, self.comment_body)