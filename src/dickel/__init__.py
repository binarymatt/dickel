import urlparse
try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs

__version__ = ('0', '2', '0')
__license__ = 'MIT'

class Request(object):
    """environ wrapper"""
    def __init__(self, environ):
        self._environ = environ
        self.method = environ.get('REQUEST_METHOD')
        self._path = environ.get('PATH_INFO','')
        self._query_string = environ.get('QUERY_STRING','')

        self.POST = self.GET = None
        if self._query_string:
            self.GET = parse_qs(self._query_string)
        if self.method == 'POST':
            self.POST = cgi.FieldStorage(fp=environ['wsgi.input'],
                                                     environ=environ,
                                                     keep_blank_values=1)
        
        def _method_get(self):
            return _method
        def _method_set(self, method):
            self._method = method
        def _method_del(self):
            self._method = None
            del self._method
        method = property(_method_get,_method_set, _method_del)

class Response(object):
    codes = {
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
    def __init__(self, content=None, status=200, headers={'Content-Type':'text/html; charset=utf8'}):
        #print headers
        #print status
        #print body
        self.status = status
        self.headers = headers
        self.content = content
        
        #self.content_type = content_type
    
    def _status_get(self):
        try:
            status_text = self.codes[self.status_code]
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
    
    def get_content(self):
        return self._content
    
    def set_content(self, value):
        self._content = value
        if value is not None:
            self.content_length = len(value)
            self._headers['Content-Length'] = str(self.content_length)
    
    def del_content(self):
        self._content = None
        self.content_length = None
    
    content = property(get_content, set_content, del_content)
    
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