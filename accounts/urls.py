from django.conf.urls import url
from .import views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm,password_reset_complete

##avoid hardcoding urls in project
##so use 'name=' in the url pattern and reverse function so that if you change
##a url from say account/login to account/users/login then you wuldnt have to change
##that url everywhere in your project rather you take advantage of the name= and reverse function

urlpatterns = [

    url(r'^login/$', login, {'template_name':'accounts/login.html'},name = 'login'),
    url(r'^logout/$', logout, {'template_name':'accounts/logout.html'}, name = 'logout'),
    url(r'^register/$', views.register,name = 'register'),
    url(r'^profile/$', views.view_profile,name = 'view_profile'),

    url(r'^profile/(?P<pk>\d+)/$', views.view_profile,name = 'view_profile_with_pk'),

    url(r'^profile/edit/$', views.edit_profile,name = 'edit_profile'),
    url(r'^change-password/$', views.change_password,name = 'change_password'),

    url(r'^reset-password/$', password_reset, {'template_name':'accounts/reset_password.html',
    'post_reset_redirect':'accounts:password_reset_done', 'email_template_name':'accounts/reset_password_email.html'}, name = 'reset_password'),

    url(r'^reset-password/done/$', password_reset_done, {'template_name': 'accounts/reset_password_done.html'}, name = 'password_reset_done'),

    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
    password_reset_confirm,{'post_reset_redirect':
    'accounts:password_reset_complete'},name ='password_reset_confirm'),

    url(r'^reset-password/complete/$',password_reset_complete, name = 'password_reset_complete'),
    
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
]

    ##url(r'^blog/(?P<pk>\d+)/$', views.view_blogpost,name = 'view_blogpost_with_pk')


## url(r'^blog/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.view_blogpost,name = 'view_blogpost')