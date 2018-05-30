from django.db import models
from django.contrib.auth.models import User
from django import forms
from django_extensions.db.fields import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum



class LikeManager(models.Manager):
    #https://docs.djangoproject.com/en/2.0/topics/db/managers/
    #Manager returns objects by querying database for every model eg Like.objects.all, can change to Like.likes.all() for example by saying likes = model.Manager() in Like model
    #Here we define custom manager called LikeManager and override the queryset that the manager returns see below
    

    use_for_related_fields = True

    def likes(self):
        # overwriting the default queryset returned by the Like Model so instead of blogpost.objects.all() we can dol 
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)
        #so we can do blogpost.likes.filter instead of blogpost.objects.filter
      
 
    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)
         
    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0
         

    def blogposts(self):
        return self.get_queryset().filter(content_type__model='blogpost').order_by('-blogposts__date')
         
 
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__date')

class Like(models.Model):
   
    LIKE = 1
    DISLIKE = -1
    VOTES = (
         (DISLIKE, 'Dislike'),
         (LIKE, 'Like')
     )
    user = models.ForeignKey(User)
    vote = models.SmallIntegerField(choices=VOTES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeManager()

    def __str__(self):
        return "%s %s" %(self.user, self.vote)



class BlogPost(models.Model):
    pic = models.ImageField(upload_to= 'profile_image', blank=True)
    title = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    body = RichTextField(config_name='awesome_ckeditor')
    slug = AutoSlugField(null=True, default=None,overwrite=True, unique=True, populate_from='title')
    votes = GenericRelation(Like, related_query_name='blogposts')

#added overwrite = True because after i changed the title of the blogpost in admin it didnt update the slug and reused the old title



    def __str__(self):
        return "%s %s %s %s " %(self.title, self.author.username, self.author.first_name, self.author.last_name)


class Comment(models.Model):
    Name = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    comment_body = models.ForeignKey(BlogPost)
    comment = models.CharField(max_length=500)
    votes = GenericRelation(Like,related_query_name='comments')

    def __str__(self):
        return "%s %s" %(self.Name, self.comment_body)




   
