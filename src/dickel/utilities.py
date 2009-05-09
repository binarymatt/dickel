import logging, sys, os
from webob.exc import *
def response_redirect(request, redirect_to):
    from webob.exc import HTTPFound
    excep = HTTPFound(location=redirect_to)
    return request.get_response(excep)

def render_response(request, template=None, context={}):
    return return_response(request, context, template)

def return_response(request, dictionary={}, template_name=None):
    """
        Takes a request and an optional dictionary and template_name
        
        request - webob.Request object.
        dictionary - any data that might need to be passed to the template
        template_name - an optional template file name for the current request
        
        If template_name is not passed, the return_response function will try
        to implicitly fine the template based on the module/function name of
        calling view.
        
        return_response uses Jinja2 templates to render html
    """
    from webob import Response
    from dickel.config import settings
    dictionary['request'] = request
    template_dir = settings.TEMPLATE_DIRECTORY
    logging.debug(template_dir)
    #response = Response()
    if template_name is None:
        #find the current frame and get caller
        f = sys._getframe(1)
        c = f.f_code
        dir_list = c.co_filename.split(os.sep)
        module_name = dir_list[-1].split('.')[0]
        func_name = c.co_name
        template_name = '%s_%s.html' % (module_name, func_name)
        logging.debug(template_name)
    #template_path = os.path.join(template_dir, template_name)
    from jinja2 import Environment, FileSystemLoader
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)
    dictionary['flash'] = request.flash
    
    body = template.render(dictionary)
    response = Response()
    response.unicode_body = body
    return response

def serve_static(request, file_name):
    import mimetypes
    import sys, os
    from dickel.config import settings
    from webob import Response
    
    response = Response()
    settings_dir = getattr(settings, 'STATIC_DIR', None)
    file_path = os.path.join(settings_dir, file_name)
    if os.path.exists(file_path):
        guess = mimetypes.guess_type(file_path)[0]
        if guess is None: 
            response.content_type = 'text/plain'
        else: 
            response.content_type = guess
        f = response.body_file
        f.write(open(file_path, 'r').read())
        return response
    else:
        excep = HTTPNotFound()
        return request.get_response(excep)

