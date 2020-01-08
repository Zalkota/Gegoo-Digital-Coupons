from functools import wraps
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

def user_is_merchant(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

            user = request.user
            if user.is_merchant == True:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
                # return HttpResponseRedirect('/')
    return wrap