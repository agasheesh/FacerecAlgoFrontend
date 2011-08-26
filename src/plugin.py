# -*- coding: utf-8 -*-

import abc
import imp
import logging
import pkgutil
import pyclbr


__all__ = ['Plugin']


def _get_all_classes_names(clbr_analysis):
    ret = set()
    for c in clbr_analysis:
        if isinstance(c, pyclbr.Class):
            ret.add(c.name)
            ret.union(_get_all_classes_names(c.super))
    return ret

def _is_a_plugin_module(mod_name, path):
    # ==========================================================================
    # CAUTION: UNSAFE AND UGLY CODE    
    # unfortunately this is needed to overpass the pyclbr cache and allow
    # checking of changed modules =/
    reload(pyclbr)
    # ==========================================================================
    superclasses_in_mod = reduce(set.union, (_get_all_classes_names(c.super) \
        for c in pyclbr.readmodule(mod_name, path).values()))
    # I know... this is not a very comprehensive and secure test because the
    # class name is not a unique identifier... but for the scope of this
    # application, it's completely OK
    return Plugin.__name__ in superclasses_in_mod


class _PluginMeta(abc.ABCMeta):

    def __init__(self, name, bases, attrs):
        super(_PluginMeta, self).__init__(name, bases, attrs)
        if not hasattr(self, '_registered'):
            self._registered = []
        else:
            self._registered.append(self)


class Plugin(object):

    __metaclass__ = _PluginMeta

    @classmethod
    def load(cls, *paths):
        paths = list(paths)
        cls._registered = []
        for _, name, _ in pkgutil.iter_modules(paths):
            if _is_a_plugin_module(name, paths):
                fid, pathname, desc = imp.find_module(name, paths)
                try:
                    imp.load_module(name, fid, pathname, desc)
                except Exception as e:
                    logging.warning("couldn't fully load plugin mod. '%s': %s",
                                    pathname, e.message)
                if fid:
                    fid.close()

    @classmethod
    def get_instances(cls):
        ret = []
        for p in cls._registered:
            try:
                ret.append(p())
            except TypeError as e:
                logging.warning("couldn't instantiate plugin class '%s': %s",
                                p.__name__, e.message)
        return ret

    @abc.abstractmethod
    def setup(self):
        pass

    @abc.abstractmethod
    def teardown(self):
        pass