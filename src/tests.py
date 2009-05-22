from webtest import TestApp
import logging
from dickel import Application
def hello_world(request):
    from webob import Response
    response = Response("Hello World")
    return response

def args_func(request, path):
    from webob import Response
    response = Reponse('Hello %s!' % path)
    return response

def redirect_func(request):
    from webob.exc import *
    return HTTPMovedPermanently('/hello/world/')

class TestDickel(object):
    def setup(self):
        urls = (
            (r'^/hello/$', hello_world),
            (r'^/world/$','tests.hello_world'),
            (r'^/hello/(?P<path>\w+)/$',args_func),
            (r'^/nohere/$',redirect_func),
        )
        logging.debug(urls)
        self.app = TestApp(Application(urls))
    def test_instance_method(self):
        res = self.app.get('/hello/')
        assert res.body == "Hello World"
        assert res.status_int == 200
    def test_string_method(self):
        res = self.app.get('/world/')
        assert res.body == "Hello World"

if __name__ == "__main__":
    import nose
    nose.main()
        