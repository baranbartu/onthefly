from django.apps import AppConfig

from onthelfy.monkey_patch import patch


class OntheflyConfig(AppConfig):
    name = 'onthelfy'
    patched = False

    def ready(self):
        if not self.patched:
            patch()
            self.patched = True
