from django.conf.urls import url, include
from django.contrib import admin
from tutorial import views
from django.conf import settings
from django.conf.urls.static import static

##namespace
##If you have multiple apps and you want to use the same urls

urlpatterns = [
    url(r'^$', views.login_redirect, name='login_redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('accounts.urls', namespace = 'accounts')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^home/', include('home.urls', namespace = 'home')),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



