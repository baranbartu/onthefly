from django.apps import AppConfig

from onthefly.monkey_patch import patch


class OntheflyConfig(AppConfig):
    name = 'onthefly'
    patched = False

    def ready(self):
        if not self.patched:
            patch()
            self.patched = True
