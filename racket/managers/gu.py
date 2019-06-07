from gevent import monkey
monkey.patch_all()

import grpc.experimental.gevent
grpc.experimental.gevent.init_gevent()


import multiprocessing
import gunicorn.app.base
from gunicorn.six import iteritems
from gevent import monkey
monkey.patch_all()

from racket.managers.server import ServerManager


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def init(self, parser, opts, args):
        pass

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def run(**kwargs):
    defaults = {
        'bind': '%s:%s' % ('0.0.0.0', '8000'),
        'workers': number_of_workers(),
        'worker_class': 'gevent',
        'use_reloader': False,
        'threaded': True
    }
    options = {**defaults, **kwargs}
    StandaloneApplication(ServerManager.create_app('prod', False), options).run()
