from feedback_wsgi import app
from feedback_wsgi.request import Request


def run(environ, start_response):
    request = Request(environ)
    action = app.dispatch(request.route)
    status, headers, response_body = action(request)
    start_response(status, headers)
    return iter([response_body.encode()])