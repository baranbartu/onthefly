import os
import imp
import json

SUPPORTED_TYPES = [int, float, str, bool, dict, list]


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


def convert(value, _type):
    # convert builtin types: int,str,float,bool,dict,list
    if _type == str:
        return value
    elif _type == bool:
        if value == 'True':
            return True
        elif value == 'False':
            return False
    elif _type in [list, dict]:
        return json.loads(value)
    elif _type == int:
        return int(value)
    elif _type == float:
        return float(value)
