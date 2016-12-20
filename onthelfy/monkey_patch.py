from django import conf
from onthelfy.backend import backend_registry


class OnTheFlySettings(object):
    def __init__(self, decoratee):
        self._decoratee = decoratee
        configuration = getattr(self._decoratee, 'ONTHEFLY', {
            'BACKEND': 'RedisBackend',
            'OPTIONS': {'URL': 'redis://localhost:6379/15'}})
        backend = configuration['BACKEND']
        options = configuration['OPTIONS']
        backend_class = backend_registry[backend]
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
