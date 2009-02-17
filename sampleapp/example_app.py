from dickel import DickelApp
if __name__ == "__main__":
    import os, sys
    path = os.path.realpath(os.path.join('../',os.path.dirname(__file__)))
    sys.path.append(path)
    os.environ["DICKEL_MOD"] = 'sampleapp.settings'
    app = DickelApp()
    try:
        from werkzeug import run_simple
        run_simple('localhost', 8000, app, use_reloader=True)
    except:
        from wsgiref.simple_server import make_server, demo_app
        server = make_server('', 8000, app)
        server.serve_forever()