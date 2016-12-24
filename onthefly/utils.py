import os
import imp


def load_class(path):
    """
    Loads class from path.
    """

    mod_name, klass_name = path.rsplit('.', 1)
    mod_args = mod_name.split('.')
    mod_args.pop(0)

    try:
        import onthefly as djonthefly
        mod_path = '%s/%s/%s.py' % (
            os.path.dirname(djonthefly.__file__), mod_args[0], mod_args[1])
        mod = imp.load_source(mod_name, mod_path)
    except AttributeError as e:
        raise ImproperlyConfigured(
            'Error importing {0}: "{1}"'.format(mod_name, e))

    try:
        klass = getattr(mod, klass_name)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "{0}" does not define a "{1}" class'.format(mod_name,
                                                                klass_name))

    return klass
