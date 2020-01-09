from functools import wraps
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

def user_is_merchant(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

            user = request.user
            if user.is_merchant == True:
                return function(self, *args, **kwargs)
            else:
                raise PermissionDenied
                # return HttpResponseRedirect('/')
    return wrap

class IsMerchantMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_merchant == True:
            return super(IsMerchantMixin, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

class IsUserObject(object):

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        if obj.merchant != user:
            raise PermissionDenied
        else:
            return super(IsMerchantMixin, self).dispatch(request, *args, **kwargs)