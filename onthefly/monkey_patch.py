from django import conf
from onthefly.utils import load_class


class OnTheFlySettings(object):
    def __init__(self, decoratee):
        self._decoratee = decoratee
        configuration = getattr(self._decoratee, 'ONTHEFLY', {
            'BACKEND': 'onthefly.backend.redis_backend.RedisBackend',
            'OPTIONS': {'URL': 'redis://localhost:6379/15'}})
        backend = configuration['BACKEND']
        options = configuration['OPTIONS']
        backend_class = load_class(backend)
        self.backend = backend_class(options, original=decoratee)

    def __getattr__(self, name):
        if name in self.backend.get_all_fields():
            return self.backend.get_value(name)
        else:
            return getattr(self._decoratee, name)

    @property
    def __module__(self):
        return self._decoratee.__module__


def patch():
    conf.settings = OnTheFlySettings(conf.settings)
