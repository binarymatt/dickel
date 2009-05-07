import sys, re, logging
from logging import getLogger
log = getLogger(__file__)
_routes = []
class LazyController(object):
    def __init__(self, module):
        if isinstance(module, basestring):
            self._smod = module
            self._mod = None
        else:
            self._mod = module
        
    def _load_controller(self, string):
        """
            loads controller from string given in the routing mechanism

            string - in the format of module.function
        """
        mod_list = string.split('.')
        if len(mod_list) > 1:
            mod = mod_list[:len(mod_list)-1]
            mod = '.'.join(mod)
            func_name = mod_list[-1]
        else:
            #i'm not sure what this would mean
            pass
        __import__(mod)
        module = sys.modules[mod]
        func = getattr(module, func_name)
        return func
    def __call__(self):
        if not self._mod:
            log.debug("importing controller, lazily. We don't like work unless we have to.")
            self._mod = self._load_controller(self._smod)
        return self._mod
    
class Dispatcher(object):
    def __init__(self):
        log.debug("initializing dispatcher")
    
    def _load_controller(self, string):
        """
            loads controller from string given in the routing mechanism
            
            string - in the format of module.function
        """
        #this is a comment
        mod_list = string.split('.')
        if len(mod_list) > 1:
            mod = mod_list[:len(mod_list)-1]
            
            mod = '.'.join(mod)
            func_name = mod_list[-1]
        else:
            #i'm not sure what this would mean
            pass
        __import__(mod)
        module = sys.modules[mod]
        func = getattr(module, func_name)
        return func
    
    @staticmethod
    def route(regex, view):
        """
        creates a route that can be matched against incoming paths
        
        regex - is the regular expression that is used to map a view to a path
        view - module.func that is used to process the request object and create response
        """
        log.debug("route: %s" % regex)
        log.debug("view: %s" % view)
        #if isinstance(view, basestring):
        controller = LazyController(view)
        global _routes
        #tup = (re.compile(regex), controller)
        tup = (regex, controller)
        _routes.append(tup)
        
    def dispatch(self, request):
        log.debug("trying to dispatch on: %s" % request.path)
        for regex, controller in _routes:
            match = re.match(regex, request.path)
            if match:
                log.debug("match found, calling controller")
                kwargs = match.groupdict()
                try:
                    response = controller()(request, **kwargs)
                except Exception, inst:
                    log.exception("Error calling controller")
                    raise inst
                return response
        raise Exception