import os
DEBUG = False
TEMPLATE_DIRECTORY = os.path.realpath(os.path.join(os.path.dirname(__file__), "templates/"))
APPS = ('sampleapp',)
URLS = (
    (r'^/counter$', 'sampleapp.views.counter'),
)