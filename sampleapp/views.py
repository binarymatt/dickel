from dickel import Response

from dickel.utilities import render_response
import config
import os, inspect, sys
from mako.template import Template
import logging

def counter(request):
    """
        Simple view taking in a dickel.Request object
    """
    if not request.session.has_key('value'):
        request.session['value'] = 0
    request.session['value'] += 1
    request.session.save()
    
    return render_response(request, 'counter.html', {'counter':request.session['value']})
