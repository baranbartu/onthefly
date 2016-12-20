backend_registry = {}


class Registry(type):
    def __new__(mcs, clsname, bases, attrs):
        new_class = super(Registry, mcs).__new__(mcs, clsname, bases, attrs)
        backend_registry[clsname] = mcs
        return new_class


class BaseBackend(object):
    __metaclass__ = Registry

    bucket_prefix = 'ONTHEFLY'

    def __init__(self, options, original=None):
        self.options = options
        self.original = original
        backend_registry[type(self).__name__] = self

    def get_value_from_original_settings(self, name):
        return getattr(self.original, name)

    def get_all_fields(self):
        raise NotImplementedError()

    def add_field(self, name):
        raise NotImplementedError()

    def set_value(self, name, value):
        raise NotImplementedError()

    def get_value(self, name):
        raise NotImplementedError()

    def get_all_values(self):
        raise NotImplementedError()

    def delete(self, name):
        raise NotImplementedError()
