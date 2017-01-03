class Backend(object):
    # should be implemented all methods
    def set(self, name, value):
        raise NotImplementedError()

    def get(self, name):
        raise NotImplementedError()

    def delete(self, name):
        raise NotImplementedError()

    def set_fields(self):
        raise NotImplementedError()

    def fields(self):
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()


class AbstractBackend(Backend):
    bucket_prefix = 'ONTHEFLY'

    def __init__(self, options, original=None):
        self.options = options
        self.original = original
        self.field_registry = None
        self.value_registry = {}

    def get_value_from_original_settings(self, name):
        return getattr(self.original, name)

    def get_fields(self):
        if self.field_registry is None:
            self.field_registry = self.fields()
        return self.field_registry

    def add_field(self, name):
        if name not in self.get_fields():
            self.field_registry.append(name)
            self.set_fields()

    def delete_field(self, name):
        if name in self.field_registry:
            self.field_registry.remove(name)
            self.set_fields()

    def set_value(self, name, value):
        if name in self.value_registry:
            del self.value_registry[name]
        return self.set(name, value)

    def get_value(self, name):
        if name in self.value_registry:
            value = self.value_registry[name]
        else:
            value = self.get(name)
            self.value_registry[name] = value
        return value

    def delete_value(self, name):
        if name in self.value_registry:
            del self.value_registry[name]
        return self.delete(name)
