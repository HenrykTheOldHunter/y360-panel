from django.contrib import admin
from .models import *
from functools import update_wrapper
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

admin.site.register(Staff)
admin.site.register(Departments)
admin.site.register(Groups)
admin.site.register(Groups_Staff)
admin.site.register(Groups_Hierarchy)
admin.site.register(Groups_Members)
admin.site.register(Domains)

def admin_view(view, cacheable=False):
    def inner(request, *args, **kwargs):
        if not request.user.is_active and not request.user.is_staff:
            raise PermissionDenied()
        return view(request, *args, **kwargs)

    if not cacheable:
        inner = never_cache(inner)
    if not getattr(view, 'csrf_exempt', False):
        inner = csrf_protect(inner)

    return update_wrapper(inner, view)
