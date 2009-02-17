from dickel.decorators import route
from dickel.utilities import render_response

@route(r'^/counter2$')
def count(request):
    if not request.session.has_key('value'):
        request.session['value'] = 0
    request.session['value'] += 1
    request.session.save()
    
    return render_response(request, 'counter.html', {'counter':request.session['value']})