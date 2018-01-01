from django.conf.urls import url
from home.views import HomeView, BlogPostView,add_blogpost
from. import views


urlpatterns =[
    url(r'^$', HomeView.as_view(), name = 'home'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name = 'change_friends'),
    url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>[-\w]+)/$', BlogPostView.as_view(),name = 'view_blogpost_with_pk'),
    url(r'^addblogpost/$', add_blogpost.as_view(), name = 'add_blogpost')
]