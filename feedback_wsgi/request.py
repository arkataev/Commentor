import cgi
from urllib.parse import parse_qs
import pickle

class Request:

    MIME_TABLE = {'txt': 'text/plain',
                  'html': 'text/html',
                  'css': 'text/css',
                  'js': 'application/javascript',
                  }
    @property
    def post(self):
        return self.__post

    @property
    def query(self):
        return self.__query

    @property
    def valid_token(self):
        return self._validate_token(self.post.getvalue('csrf'))

    @property
    def is_static(self):
        return 'static' in self.route

    @property
    def content_type(self):
        file_name = self.route.split('/')[-1]
        return self.MIME_TABLE.get(file_name.split('.')[-1])

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
            else: return False