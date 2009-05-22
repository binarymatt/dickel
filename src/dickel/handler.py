#from dickel import Request, Response
#from dickel import Request, Response
from webob import Request, Response
from webob.exc import *

from dickel.dispatch import Dispatcher

import os
import logging

class Application(object):
    def __init__(self, urls=None):
        self.dispatcher = Dispatcher()
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d - %(message)s',level=logging.DEBUG)

        self.log = logging.getLogger('dickel.app')
        logging.getLogger('dickel.dispatch').setLevel(logging.DEBUG)
        self.log.setLevel(logging.DEBUG)
        for a,b in urls:
            Dispatcher.route(a,b)
        
    def __call__(self, environ, start_response):
        #request = Request(environ)
        #return request.get_response(self._internal_app)
        return self._internal_app(environ, start_response)

    def _internal_app(self, environ, start_response):
        request = Request(environ)
        response = self.get_response(request)
        return response(environ, start_response)
        #start_response(response.status, response.headers)
        #return response.content
    
    def get_response(self, request):
        try:
            self.log.debug("Trying dispatcher")
            response = self.dispatcher.dispatch(request)
        except Exception, inst:
            self.log.exception('errors')
            exc = HTTPNotFound()
            response = request.get_response(exc)
        return response
