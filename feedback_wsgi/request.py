import cgi
from urllib.parse import parse_qs
import pickle

class Request:

    @property
    def post(self):
        return self.__post

    @property
    def query(self):
        return self.__query

    @property
    def valid_token(self):
        return self._validate_token(self.post.getvalue('csrf'))

    def __init__(self, env):
        self.route = env['PATH_INFO']
        self.method = env['REQUEST_METHOD']
        self.__query = parse_qs(env['QUERY_STRING'])
        self.__post = cgi.FieldStorage(fp=env['wsgi.input'], environ=env)

    def _validate_token(self,token):
        with open('cache.txt', 'rb+') as f:
            cached_token = pickle.load(f).get('token')
            if cached_token == token:
                f.truncate(0)
                return True
            else:
                return False