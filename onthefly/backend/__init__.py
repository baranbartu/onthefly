class Backend(object):
    # should be implemented all methods
    # todo write method docstrings
    def _set_value(self, name, value):
        raise NotImplementedError()

    def _get_value(self, name):
        raise NotImplementedError()

    def _delete_value(self, name):
        raise NotImplementedError()

    def set_fields(self):
        raise NotImplementedError()

    def get_fields(self):
        raise NotImplementedError()

    def get_values(self):
        raise NotImplementedError()


class AbstractBackend(Backend):
    bucket_prefix = 'ONTHEFLY'

    def __init__(self, options, original=None):
        self.options = options
        self.original = original
        self._all_fields = None
        self.registry = {}

    @property
    def all_fields(self):
        if not self._all_fields:
            self._all_fields = self.get_fields()
        return self._all_fields

    def add_field(self, name):
        if name not in self.all_fields:
            self._all_fields.append(name)
            self.set_fields()

    def delete_field(self, name):
        if name in self._all_fields:
            self._all_fields.remove(name)
            self.set_fields()

    def get_value_from_original_settings(self, name):
        return getattr(self.original, name)

    def set_value(self, name, value):
        if name in self.registry:
            del self.registry[name]
        return self._set_value(name, value)

    def get_value(self, name):
        if name in self.registry:
            value = self.registry[name]
        else:
            value = self._get_value(name)
            self.registry[name] = value
        return value

    def delete_value(self, name):
        if name in self.registry:
            del self.registry[name]
        return self._delete_value(name)
