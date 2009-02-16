import os
class SettingsMod(object):
    def __init__(self):
        self._module = None
    def __getattr__(self, attr):
        if self._module is None:
            self._import_mod()
        return getattr(self._module, attr)
    
    def _import_mod(self):
        try:
            settings_module = os.environ["DICKEL_MOD"]
            if settings_module is None:
                raise KeyError
            self._module = __import__(settings_module, {}, {}, [''])
        except KeyError, k:
            raise ImportError, "Could not import settings module"
        except ImportError, e:
            raise ImportError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (self.SETTINGS_MODULE, e)
            
settings = SettingsMod()