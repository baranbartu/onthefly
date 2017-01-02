from django import conf
from django.views.debug import get_safe_settings
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
        if name in self.backend.all_fields:
            return self.backend.get_value(name)
        else:
            return getattr(self._decoratee, name)

    @property
    def __module__(self):
        return self._decoratee.__module__

    @property
    def get_original_settings_without_onthefly(self):
        all_settings = get_safe_settings().keys()
        original_settings_without_onthefly = set(all_settings).difference(
            self.backend.all_fields)
        return list(original_settings_without_onthefly)

    @property
    def get_onthefly_settings(self):
        return self.backend.get_values()


def patch():
    conf.settings = OnTheFlySettings(conf.settings)
