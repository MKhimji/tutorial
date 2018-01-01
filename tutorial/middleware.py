##Instead of using @login_required func in all our views so that anon users cant access certain pages
##Use middleware to check if views can be accessed by users depending on if they are authenticated or not
##middleware lies in the middle of the request response cycle so that before a response is given, the middleware
##is run to check any conditions before the view is processed i.e process view function.

import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout


## compiles a list of regular expressions that are exempt i.e will not redirect to the login page
## first EXEMPT_URLS is only referring to /account/login in settings.LOGIN_URL. So obviously theres no point redirecting to the login page
##when that the actual page that we're on.
## lstrip removes the first / in '/account/login' in settings.LOGIN_URL
##so altogether the 3 lines exclude the user from being redirected to the login page if the user is in the login logout or register pages.

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


##process view standard django function used in middleware  so for example
##before the view_profile template is rendered it will check to see if there are any conditions
##which must be met
##path is the url which the user is trying to access

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response


##request is an object which has lot of useful info about the user one of them is
##path_info which tells us what url the user is trying to get.


    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')



##url_is_exempt returns boolean value true or false

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)
##name = 'logout' in reverse object from urls to avoid hardooding
##need l strip again because reverse us returning the string /account/logout
##and we are comparing it to the path variable in process_view which returns account/logout
##so we need to remove the first / before

##accounts : referring to namespace accounts

        if path == reverse('accounts:logout').lstrip('/'):
            logout(request)
##reverse gives a string

##if user is logged in and is trying to access one of the exempt urls redirect them to the homepage
        if request.user.is_authenticated() and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)

##if user is authenticated or url is exempt ( so could be not authenticated but the url could be exempt
        elif request.user.is_authenticated() or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_URL)
