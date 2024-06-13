import importlib
import os
import sys
import types


def reload_package(package):
    assert hasattr(package, "__package__")
    fn = package.__file__
    fn_dir = os.path.dirname(fn) + os.sep
    module_visit = {fn}
    del fn

    def reload_recursive_ex(module):
        importlib.reload(module)

        for module_child in vars(module).values():
            if isinstance(module_child, types.ModuleType):
                fn_child = getattr(module_child, "__file__", None)
                if (fn_child is not None) and fn_child.startswith(fn_dir):
                    if fn_child not in module_visit:
                        # print("reloading:", fn_child, "from", module)
                        module_visit.add(fn_child)
                        reload_recursive_ex(module_child)

    return reload_recursive_ex(package)


def reload_class(instance):
    cls = instance.__class__
    modname = cls.__module__
    del sys.modules[modname]

    module = __import__(modname)
    submodules = modname.split(".")[1:]

    for submodule in submodules:
        module = getattr(module, submodule)

    instance.__class__ = getattr(module, cls.__name__)
