class BaseBackend(object):
    bucket_prefix = 'ONTHEFLY'

    def __init__(self, options, original=None):
        self.options = options
        self.original = original
        self._all_fields = None

    @property
    def all_fields(self):
        if not self._all_fields:
            self._all_fields = self.get_all_fields()
        return self._all_fields

    def add_field(self, name):
        if name not in self.all_fields:
            self._all_fields.append(name)
            self.set_fields()
            original_value = self.get_value_from_original_settings(name)
            self.set_value(name, original_value)

    def delete_field(self, name):
        if name in self._all_fields:
            self._all_fields.remove(name)
            self.set_fields()
            self.delete_value(name)

    def get_value_from_original_settings(self, name):
        return getattr(self.original, name)

    def set_fields(self):
        raise NotImplementedError()

    def set_value(self, name, value):
        raise NotImplementedError()

    def get_value(self, name):
        raise NotImplementedError()

    def get_all_values(self):
        raise NotImplementedError()

    def delete_value(self, name):
        raise NotImplementedError()
