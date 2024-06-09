from twirp.asgi import TwirpASGIApp
from starlette.middleware.cors import CORSMiddleware

def init_server(services:list,
                allow_origins=[],
                allow_methods=[],
                allow_headers=[]):
    
    app = TwirpASGIApp()   
    for service in services:
        app.add_service(service)



    # Wrap the app with CORSMiddleware
    app = CORSMiddleware(
    app,
    allow_origins=allow_origins,
    allow_methods=allow_methods,
    allow_headers=allow_headers,
    )

    return app