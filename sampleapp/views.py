from dickel import Response
import logging

def hello_world(request):
    response = Response("Hello World")
    return response

