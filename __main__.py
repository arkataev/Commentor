try:
    import os
    import gunicorn
except ImportError:
    os.system('pip install -r .requirements.txt')

import gunicorn.app.base
from gunicorn.six import iteritems
import multiprocessing
from wsgi import run

HOST = '127.0.0.1'


class CommentorApp(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(CommentorApp, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    options = {
        'bind': '%s:%s' % (HOST, '8080'),
        'workers': multiprocessing.cpu_count() * 2 + 1,
        'access_log_format': "%(h)s %(q)s %(U)s %(s)s %(b)s"
    }

    CommentorApp(run, options).run()