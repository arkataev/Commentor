from feedback_wsgi import app
import cgi


def run(environ, start_response):
    route = environ['PATH_INFO']
    form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
    action = app.dispatch(route)
    data = {'token': form.getvalue('csrf')} # testing csrf token
    status, headers, response_body = action(**data)
    start_response(status, headers)
    return iter([response_body.encode()])