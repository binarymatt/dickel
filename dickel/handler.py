#from dickel import Request, Response
from webob import Request, Response
from dickel.dispatch import Dispatcher
from dickel.config import settings
from utilities import Flash
import os
import logging

class DickelApp(object):
    def __init__(self, app=None, urls=None):
        if app is None:
            #create our internal app
            self.app = self._internal_app
        else:
            self.app = app
        from beaker.middleware import SessionMiddleware
        from middleware import SqlAlchemyMiddleware
        self.app = SqlAlchemyMiddleware(self.app)
        
        self.app = SessionMiddleware(self.app, key='key', secret='secret')
        self.dispatcher = Dispatcher()
        logging.basicConfig(format='%(asctime)s %(levelname)s %(module)s.%(funcName)s:%(lineno)d - %(message)s',level=logging.DEBUG)

        self.log = logging.getLogger('dickel.app')
        if settings.DEBUG:
            logging.getLogger('dickel.dispatch').setLevel(logging.DEBUG)
        self.log.setLevel(logging.DEBUG)
        if urls is None:
            urls = getattr(settings, 'URLS',[])
        apps = getattr(settings,'APPS')
        for app in apps:
            try:
                __import__('%s.controller'% app, {}, {}, [''])
            except:
                if settings.DEBUG:
                    self.log.exception("error")
                pass
        for a,b in urls:
            Dispatcher.route(a,b)
        
    def __call__(self, environ, start_response):
        return self.app(environ, start_response)

    def _internal_app(self, environ, start_response):
        from dickel.config import settings
        request = Request(environ)
        request.flash = Flash()
        if environ.has_key('dickel.samiddleware'):
            request.sa_session = environ['dickel.samiddleware']
        if environ.has_key('beaker.session'):
            request.session = environ['beaker.session']
        
        initializers = getattr(settings, 'INITIALIZERS', [])
        for st in initializers:
            ar = st.split('.')
            mod_name = '.'.join(ar[:-1])
            func_name = ar[-1]
            try:
                mod = __import__(mod_name, {}, {}, [''])
                func = getattr(mod, func_name)
                func(request)
            except ImportError, e:
                self.log.exception("Error calling import in initializer")
        
        response = self.get_response(request)
        destroyers = getattr(settings, 'DESTROYERS', [])
        for dest in destroyers:
            ar = dest.split('.')
            mod_name = '.'.join(ar[:-1])
            func_name = ar[-1]
            try:
                mod = __import__(mod_name, {}, {}, [''])
                func = getattr(mod, func_name)
                func(request)
            except ImportError, e:
                self.log.exception("Error calling import in destroyer")
        return response(environ, start_response)
    
    def get_response(self, request):
        try:
            response = self.dispatcher.dispatch(request)
        except Exception, inst:
            if settings.DEBUG:
                #show a debug page
                from jinja2 import Environment, FileSystemLoader
                import os
                template = os.path.join(os.path.dirname(os.path.abspath(__file__)),'templates')
                self.log.debug(template)
                env = Environment(loader=FileSystemLoader(template))
                template = env.get_template('debug_exception.html')
                dictionary = {
                    'headers':request.headers,
                    'get_vars':request.GET,
                    'post_vars':request.POST,
                    'urls':settings.URLS
                }
                body = template.render(dictionary)
                response = Response(body=body)
            else:
                from webob.exc import HTTPNotFound
                excep = HTTPNotFound()
                response = request.get_response(excep)
        return response
