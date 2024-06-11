# Python
import json

# Django
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View as DjangoView
from django.http import HttpRequest

class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs) # type: ignore
    
class View(DjangoView):

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.method == "PUT":
            request.PUT = json.loads(request.body.decode('utf-8').replace("'", '"')) # type: ignore
        elif request.method == "DELETE":
            request.DELETE = json.loads(request.body.decode('utf-8').replace("'", '"')) # type: ignore
        return super().dispatch(request, *args, **kwargs)