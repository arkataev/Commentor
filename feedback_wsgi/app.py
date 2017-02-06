from .response import page_not_found
from functools import partial
import pickle
from . import controller
import hashlib
import os

def dispatch(route):
    return {
        '/comment': partial(controller.comment, csrf=_set_token()),
        '/stats': controller.view_stats,
        '/view': controller.view_comments,
        '/save_comment': controller.add_comment,
        '/delete_comment': controller.delete_comment,
        '/get_locations': controller.get_locations,
    }.get(route, partial(page_not_found, fname='not_found.html'))

def validate_token(token):
    with open('cache.txt', 'rb+') as f:
        cached_token = pickle.load(f).get('token')
        if cached_token == token:
            f.truncate(0)
            return True
        else: return False

def _set_token():
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
