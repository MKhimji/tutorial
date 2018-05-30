from django.conf.urls import url
from  .import views
from home.models import BlogPost, Comment, Like
from home.views import VotesView



urlpatterns =[
    url(r'^$',views.home, name = 'home'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/$', 
    views.blog,
    name = 'view_blogpost_with_pk'),
    
    url(r'^blog/$',views.djangoarticles, name = 'djangoarticles'),
    
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/ajax/like/$',VotesView.as_view(model=BlogPost, vote_type=Like.LIKE),
           name='blog_like'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/ajax/dislike/$', VotesView.as_view(model=BlogPost, vote_type=Like.DISLIKE),
           name='blog_dislike'),  

]