import hashlib, inspect
from importlib import import_module
from types import BuiltinFunctionType, BuiltinMethodType

from mtb.core import mklog

log = mklog(__name__)


def hash_function(func):
    # code = func.__code__.co_code
    code = inspect.getsource(func)
    log.debug(f"Hashing function code: {code}")
    return hashlib.md5(code.encode("utf-8")).hexdigest()


from typing import Any, Callable, Dict, Tuple


def apply_patches(PATCHES: Dict[Tuple[str], Dict[str, Callable[..., Any]]], enable: bool = True):
    log.debug(f"Entering apply_patches, enable={enable}")

    for cls_full_names, methods in PATCHES.items():
        for cls_full_name in cls_full_names:
            module_name, cls_name = cls_full_name.rsplit(".", 1)

            try:
                # Import class dynamically
                log.debug(f"Importing module: {module_name}")
                module = import_module(module_name)
                cls = getattr(module, cls_name)
                log.debug(f"Successfully imported class: {cls_name}")

            except ImportError:
                log.warning(
                    f"Could not import class {cls_name} from module {module_name}. Skipping."
                )
                continue  # Skip if the class is not found
            if isinstance(cls, (BuiltinFunctionType, BuiltinMethodType)):
                raise ValueError(f"{cls} is a built-in type. Standard patching won't work.")

            for method_name, func in methods.items():
                log.debug(f"{cls}, looking for {method_name}")
                existing_method = getattr(cls, method_name, None)
                log.debug(f"{cls} id from patch_qt: {id(cls)}")

                log.debug(f"Existing method: {existing_method}")

                if enable:
                    log.debug(f"Patching method {method_name} into class {cls_name}")
                    if existing_method and not getattr(existing_method, "_patched", False):
                        existing_hash = hash_function(existing_method)
                        new_hash = hash_function(func)
                        log.debug(f"Existing hash: {existing_hash}, New hash: {new_hash}")

                        if existing_hash != new_hash:
                            raise RuntimeError(
                                f"Method {method_name} already exists in {cls} and is not a patched method. Cannot override."
                            )
                    setattr(cls, method_name, func)
                    setattr(func, "_patched", True)
                else:
                    if existing_method and getattr(existing_method, "_patched", False):
                        log.debug(f"Removing method {method_name} from class {cls_name}")
                        delattr(cls, method_name)
