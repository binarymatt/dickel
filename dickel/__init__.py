STATUS_CODE_TEXT = {
    100: 'CONTINUE',
    101: 'SWITCHING PROTOCOLS',
    200: 'OK',
    201: 'CREATED',
    202: 'ACCEPTED',
    203: 'NON-AUTHORITATIVE INFORMATION',
    204: 'NO CONTENT',
    205: 'RESET CONTENT',
    206: 'PARTIAL CONTENT',
    300: 'MULTIPLE CHOICES',
    301: 'MOVED PERMANENTLY',
    302: 'FOUND',
    303: 'SEE OTHER',
    304: 'NOT MODIFIED',
    305: 'USE PROXY',
    306: 'RESERVED',
    307: 'TEMPORARY REDIRECT',
    400: 'BAD REQUEST',
    401: 'UNAUTHORIZED',
    402: 'PAYMENT REQUIRED',
    403: 'FORBIDDEN',
    404: 'NOT FOUND',
    405: 'METHOD NOT ALLOWED',
    406: 'NOT ACCEPTABLE',
    407: 'PROXY AUTHENTICATION REQUIRED',
    408: 'REQUEST TIMEOUT',
    409: 'CONFLICT',
    410: 'GONE',
    411: 'LENGTH REQUIRED',
    412: 'PRECONDITION FAILED',
    413: 'REQUEST ENTITY TOO LARGE',
    414: 'REQUEST-URI TOO LONG',
    415: 'UNSUPPORTED MEDIA TYPE',
    416: 'REQUESTED RANGE NOT SATISFIABLE',
    417: 'EXPECTATION FAILED',
    500: 'INTERNAL SERVER ERROR',
    501: 'NOT IMPLEMENTED',
    502: 'BAD GATEWAY',
    503: 'SERVICE UNAVAILABLE',
    504: 'GATEWAY TIMEOUT',
    505: 'HTTP VERSION NOT SUPPORTED',
}
class Request(object):
    def __init__(self, environ):
        self.method = environ.get('REQUEST_METHOD')
        self._path = environ.get('PATH_INFO')
        self._query_string = environ.get('QUERY_STRING')
        self._content_type = environ.get('CONTENT_TYPE')
        
        for key,value in environ.items():
            #print '%s:%s' % (key, value)
            setattr(self,str(key).lower(),value)
        
        def _method_get(self):
            return _method
        def _method_set(self, method):
            self._method = method
        def _method_del(self):
            self._method = None
            del self._method
        method = property(_method_get,_method_set, _method_del)

class Response(object):
    def __init__(self, body=None, status=200, headers={'Content-Type':'text/html; charset=utf8'}):
        #print headers
        #print status
        #print body
        self.status = status
        self.headers = headers
        self.body = body
        
        #self.content_type = content_type
    
    def _status_get(self):
        try:
            status_text = STATUS_CODE_TEXT[self.status_code]
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        return '%s %s' % (self.status_code, status_text)
    
    def _status_set(self, status):
        if not isinstance(status, int):
            raise TypeError("You must set status to an integer (not %s)" % type(status))
        self.status_code = status
    
    def _status_del(self):
        self.status_code = None
    
    status = property(_status_get, _status_set, _status_del)
    
    def _body_getattr(self):
        
        return self._body
    
    def _body_setattr(self, value):
        self._body = value
        if value is not None:
            self.content_length = len(value)
            self._headers['Content-Length'] = str(self.content_length)
    
    def _body_del(self):
        self._body = None
        self.content_length = None
    
    body = property(_body_getattr,_body_setattr, _body_del)
    
    def _headers_get(self):
        return [(key,value) for key,value in self._headers.items()]
    
    def _headers_set(self, value):
        self._headers = None
        if not isinstance(value, dict):
            raise TypeError("You must set headers to a dictionary like object")
        self._headers = value
    
    headers = property(_headers_get, _headers_set)
        
    def __call__(self):
        return [self.body]
from handler import DickelApp
__all__ = ['Request','Response','DickelApp']