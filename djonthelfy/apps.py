from django.apps import AppConfig

from djonthelfy.monkey_patch import patch


class DjOntheflyConfig(AppConfig):
    name = 'djonthelfy'
    patched = False

    def ready(self):
        if not self.patched:
            patch()
            self.patched = True
