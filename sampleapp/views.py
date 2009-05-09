from dickel import Response
from dickel.decorators import route
import logging

@route(r'^/hello2$')
def hello_world(request):
    response = Response("Hello World")
    return response

