from dispatch import Dispatcher
def route(url, method=('GET','POST')):
    """
        wraps a controller function with a route.
        
        url - regex of the url to map the controller function to
        metho - TBD
    """
    def wrap(f):
        Dispatcher.route(url, f)
    return wrap
