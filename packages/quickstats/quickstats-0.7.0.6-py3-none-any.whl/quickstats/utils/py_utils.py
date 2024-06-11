import gc
import sys
import inspect

def get_required_args(obj):
    sig = inspect.signature(obj)
    required_args = [
        name for name, param in sig.parameters.items()
        if param.default is param.empty and
        param.kind in [param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY]
    ]

    # remove self in case of a class object
    if isinstance(obj, type):
        required_args = required_args[1:]

    return required_args

def get_reference_count(obj):
    return sys.getrefcount(obj)

def get_referrers(obj):
    return gc.get_referrers(obj)