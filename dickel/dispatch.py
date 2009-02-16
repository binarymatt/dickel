import sys, re, logging
_routes = []
class LazyController(object):
    def __init__(self, module_string):
        self._smod = module_string
        self._mod = None
        self.log = logging.getLogger('dickel.dispatch')
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
    def __call__(self):
        if not self._mod:
            self.log.debug("importing controller, lazily. We don't like work unless we have to.")
            self._mod = self._load_controller(self._smod)
        return self._mod
    
class Dispatcher(object):
    def __init__(self):
        self.log = logging.getLogger('dickel.dispatch')
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
    
    def route(self, regex, view):
        """
        creates a route that can be matched against incoming paths
        
        regex - is the regular expression that is used to map a view to a path
        view - module.func that is used to process the request object and create response
        """
        self.log.debug("route: %s" % regex)
        self.log.debug("view: %s" % view)
        if isinstance(view, basestring):
            controller = LazyController(view)
            global _routes
            tup = (re.compile(regex), controller)
            _routes.append(tup)
        
    def dispatch(self, request):
        self.log.debug("trying to dispatch on: %s" % request.path)
        for regex, controller in _routes:
            match = regex.match(request.path)
            if match:
                self.log.debug("match found, calling controller")
                kwargs = match.groupdict()
                try:
                    response = controller()(request, **kwargs)
                except Exception, inst:
                    self.log.exception("Error calling controller")
                    raise inst
                return response
        raise Exception