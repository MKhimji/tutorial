from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.

##UserProfileManager inherits from models.Manager
##So it inherits it's methods
##So super().get_queryset() is calling the method get_queryset from the models.Manager class and
##then we are customizing the output.

##The reason for making is a class is incase we have to do this operation lots of times it would be
##tiresome to have to include it everytime and write UserProfile.objects.filter(city = 'London') everytime so
##just associate the UserProfileManager with a filter (London in this case)
##in the UserProfile class by writing London = UserProfileManager()

class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')




##Each model is one structure on one table on the database
##userprofile is a name that we made up but the elements of this class inherit from models.Model
##So basically we are telling django that we are creating a class which is a django model and
##will be one table in our database
##class UserImage(User):
##    image = models.ImageField(upload_to= 'profile_image', blank=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=100,default='')
    website = models.URLField(default='')
    phone = models.IntegerField(default=0)
    image = models.ImageField(upload_to= 'profile_image', blank=True)

    london = UserProfileManager()
    objects = models.Manager()
##def below changes the string from UserObject to username in admin

    def __str__(self):
        return "%s" %(self.user)

##We want a UserProfile object created everytime we create a user
##Signals
##If the event was having just saved a new User object.
##when that event happens, you are able to do something based on that.
##So, in this case that thing was creating an associated UserProfile object.


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)





##create_profile stuff, sender = user from post_save connect below
##if kwargs created just means if user object has been created then create the user profile
##instance is current user



##Django will save the user object thats been created and then it will run the
##post_save signal(which takes the create_profile function above) to create a userprofile object associated with that user






