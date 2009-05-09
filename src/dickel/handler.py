#from dickel import Request, Response
from dickel import Request, Response
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
        return self._internal_app(environ, start_response)

    def _internal_app(self, environ, start_response):
        request = Request(environ)
        
        response = self.get_response(request)
        start_response(response.status, response.headers)
        return response.content
    
    def get_response(self, request):
        try:
            self.log.debug("Trying dispatcher")
            response = self.dispatcher.dispatch(request)
        except Exception, inst:
            self.log.exception('errors')
            response = Response(content='<h1>Page Not Found</h1>', status=404)
        return response
