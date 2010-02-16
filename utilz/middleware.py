from django.conf import settings
from django.http import HttpResponseServerError

class AjaxExceptionResponse(object):
   def process_exception(self, request, exception):
       if request.is_ajax():
           if settings.DEBUG:
                   import sys, traceback
                   (exc_type, exc_info, tb) = sys.exc_info()
                   response = "%s\n" % exc_type.__name__
                   response += "%s\n\n" % exc_info
                   response += "TRACEBACK:\n"
                   for tb in traceback.format_tb(tb):
                       response += "%s\n" % tb
                   return HttpResponseServerError(response)
           else:
                   return HttpResponseServerError('500')

