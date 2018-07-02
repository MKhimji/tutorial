from django.conf.urls import url
from  .import views
from home.models import BlogPost, Comment, Like
from home.views import VotesView, BlogPostYearArchiveView, BlogPostMonthArchiveView





urlpatterns =[
    url(r'^$',views.home, name = 'home'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/$', 
    views.blog,
    name = 'view_blogpost_with_pk'),
    
    # url(r'^blog/$',views.archive, name = 'archive'),
    
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/ajax/like/$',VotesView.as_view(model=BlogPost, vote_type=Like.LIKE),
           name='blog_like'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/ajax/dislike/$', VotesView.as_view(model=BlogPost, vote_type=Like.DISLIKE),
           name='blog_dislike'),  
    url(r'^(?P<year>[0-9]{4})/$',
        BlogPostYearArchiveView.as_view(),
        name="blogpost_year_archive"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/$',
        BlogPostMonthArchiveView.as_view(),
        name="blogpost_month_archive")
]