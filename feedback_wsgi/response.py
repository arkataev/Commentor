from feedback_wsgi.template import Renderer
import json
import hashlib
import os
import pickle


def response(status='200', content_type='text/html', cookie:dict=None):
    def response_wrapper(func):
        def response_body(*args, **kwargs):
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-type', content_type),
            ]
            if cookie:
                for key, value in cookie.items():
                    response_headers.append(('Set-Cookie', str(key) + '={}'.format(value)))
            r_body = func(*args, **kwargs)
            response_headers.append(('Content-Length', str(len(r_body.encode()))))
            return status, response_headers, r_body
        return response_body
    return response_wrapper

@response()
def render(fname, **kwargs):
    return Renderer().render(fname, **kwargs)

@response(content_type='application/json')
def success_json(data):
    return json.dumps(data, ensure_ascii=False)

@response(status='402',content_type='application/json')
def restricted_json(data):
    return json.dumps(data)

@response(status='404')
def page_not_found(fname, **kwargs):
    return Renderer().render(fname, **kwargs)

def set_token():
    try:
        # check if token already set
        with open('cache.txt', 'rb+') as f:
            cached_token = pickle.load(f)
            token = cached_token['token']
    except EOFError:
        # generate new token and save
        token = _get_token(os.urandom(10))
        _cache({'token': token})
    return token

def _get_token(token):
    h = hashlib.md5()
    h.update(token)
    return h.hexdigest()

def _cache(data):
    with open('cache.txt', 'wb+') as f:
        pickle.dump(data, f)
    return True