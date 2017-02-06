from feedback_wsgi.template import Renderer
import json


def response(status='200', content_type='text/html', cookie:dict=None):
    response_headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Content-type', content_type),
    ]
    if cookie:
        for key, value in cookie.items():
            response_headers.append(('Set-Cookie', str(key) + '={}'.format(value)))
    def response_wrapper(func):
        def response_body(*args, **kwargs):
            r_body = func(*args, **kwargs)
            response_headers.append(('Content-Length', str(len(r_body))))
            return status, response_headers, r_body
        return response_body
    return response_wrapper

@response()
def render(fname, **kwargs):
    return Renderer().render(fname, **kwargs)

@response(content_type='application/json')
def json_response(**kwargs):
    return json.dumps(kwargs)

@response(status='404')
def page_not_found(fname, **kwargs):
    return Renderer().render(fname, **kwargs)
