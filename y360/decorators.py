from django.http import HttpResponseBadRequest
def apply_permissions(view_func): #не пускает по серверным ссылкам (кроме аяксов)
    def _wrapped_view(request, *args, **kwargs):
        permissions = [
            is_ajax(request=request),
        ]
        if not all(permissions):
            return HttpResponseBadRequest()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'