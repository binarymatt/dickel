from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine


class SqlAlchemyMiddleware(object):
    def __init__(self, app):
        self.wsgi_app = app
    def __call__(self, environ, start_response):
        from dickel.config import settings
        Session = scoped_session(sessionmaker(autocommit=True, autoflush=True))
        if getattr(settings, 'DB_URL', None):
            engine = create_engine(settings.DB_URL, echo=True)
            Session.configure(bind=engine)
            session = Session()
            environ['dickel.samiddleware'] = session
            
        app = self.wsgi_app(environ, start_response)
        if Session.bind:
            Session.bind.dispose()
        #del environ['dickel.samiddleware']
        return app
            
        
        