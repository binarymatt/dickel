if __name__ == "__main__":
    import os, sys
    path = os.path.realpath(os.path.join('../src/',os.path.dirname(__file__)))
    print path
    sys.path.append(path)
    from dickel import Application
    from views import hello_world
    urls = (
        (r'^/hello$', hello_world),
        (r'^/world$','views.hello_world'),
    )
    app = Application(urls)
    try:
        from werkzeug import run_simple
        run_simple('localhost', 8000, app, use_reloader=True)
    except:
        from wsgiref.simple_server import make_server, demo_app
        server = make_server('', 8000, app)
        server.serve_forever()