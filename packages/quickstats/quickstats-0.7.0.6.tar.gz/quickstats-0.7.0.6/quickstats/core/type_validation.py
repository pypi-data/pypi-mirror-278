from collections import abc
from functools import cache
import types
from typing import Any, Callable, Dict, List, Tuple, Union, get_args, get_origin

# types.UnionType requires python 3.10+
try:
    from types import UnionType
    union_like_types = {Union, UnionType}
except ImportError:
    union_like_types = {Union}

class ValidatorFactory:
    """
    A factory class for creating validators that check if objects match specified type hints.

    Example Usage:

    Validate an integer list:
    ```
    validator = ValidatorFactory.get_validator(List[int])
    print(validator([1, 2, 3]))  # Expected: True
    ```

    Validate a dictionary with string keys and integer values:
    ```
    validator = ValidatorFactory.get_validator(Dict[str, int])
    print(validator({'key': 1}))  # Expected: True
    ```

    Validate a tuple of fixed types:
    ```
    validator = ValidatorFactory.get_validator(Tuple[int, str])
    print(validator((1, 'a')))  # Expected: True
    ```

    Validate a variable-length tuple of integers:
    ```
    validator = ValidatorFactory.get_validator(Tuple[int, ...])
    print(validator((1, 2, 3)))  # Expected: True
    ```
    """
    
    @staticmethod
    @cache
    def create_union_validator(type_args):
        non_generic_types = tuple(arg for arg in type_args if not get_args(arg))
        generic_type_validators = [ValidatorFactory.get_validator(arg) for arg in type_args if get_args(arg)]
        
        def validate(source):
            return isinstance(source, non_generic_types) or any(validator(source) for validator in generic_type_validators)
        
        return validate

    @staticmethod
    @cache
    def create_sequence_validator(type_arg, container_type=(list, tuple)):
        item_validator = ValidatorFactory.get_validator(type_arg[0]) if type_arg else lambda x: True
        
        def validate(source):
            return isinstance(source, container_type) and all(item_validator(item) for item in source)
        
        return validate

    @staticmethod
    @cache
    def create_dict_validator(type_args):
        if not type_args:
            return lambda source: isinstance(source, dict)
        key_validator, value_validator = map(ValidatorFactory.get_validator, type_args)
        
        def validate(source):
            return isinstance(source, dict) and all(key_validator(k) and value_validator(v) for k, v in source.items())
        
        return validate

    @staticmethod
    @cache
    def create_tuple_validator(type_args):
        if not type_args:
            return lambda source: isinstance(source, tuple)
        elif len(type_args) == 2 and type_args[1] is Ellipsis:
            item_validator = ValidatorFactory.get_validator(type_args[0])
            return lambda source: isinstance(source, tuple) and all(item_validator(item) for item in source)
        else:
            validators = [ValidatorFactory.get_validator(arg) for arg in type_args]
            def validate(source):
                return isinstance(source, tuple) and len(source) == len(validators) and all(validator(item) for validator, item in zip(validators, source))
            return validate

    @staticmethod
    @cache
    def get_validator(type_hint) -> Callable:
        """
        Retrieves a validator function for a given type hint.

        Args:
            type_hint: The type hint for which to retrieve the validator.

        Returns:
            A validator function that can be used to check if an object matches the type hint.
        """
        origin = get_origin(type_hint)
        args = get_args(type_hint)
        
        if origin in {list, abc.Sequence} and not issubclass(origin, tuple):  # exclude tuples from sequence validator
            return ValidatorFactory.create_sequence_validator(args)
        elif origin == dict:
            return ValidatorFactory.create_dict_validator(args)
        elif origin in union_like_types:
            return ValidatorFactory.create_union_validator(args)
        elif origin == tuple:
            return ValidatorFactory.create_tuple_validator(args)
        elif type_hint == Any:
            return lambda _: True
        else:
            return lambda source: isinstance(source, type_hint)

get_type_validator = ValidatorFactory.get_validator

def check_type(obj, type_hint):
    """
    Checks if an object matches a given type hint.
    
    Args:
        obj: The object to be checked.
        type_hint: The type hint against which the object is to be validated.

    Returns:
        bool: True if the object matches the type hint, False otherwise.

    Examples:
        Check if a list only contains integers:
        >>> check_type([1, 2, 3], List[int])
        True

        Check if a variable is either a string or a list of strings:
        >>> check_type("hello", Union[str, List[str]])
        True
        >>> check_type(["hello", "world"], Union[str, List[str]])
        True

        Validate a dictionary with string keys and integer values:
        >>> check_type({'key': 42}, Dict[str, int])
        True

        Check against a tuple with specified types:
        >>> check_type((1, 'a'), Tuple[int, str])
        True

        Validate a variable-length tuple of integers:
        >>> check_type((1, 2, 3, 4), Tuple[int, ...])
        True

    Note: The method will return False if the object does not match the type hint:
        >>> check_type([1, 'a', 3], List[int])
        False
        >>> check_type({'key': 'value'}, Dict[str, int])
        False
    """
    return get_type_validator(type_hint)(obj)

@cache
def get_type_hint_str(type_hint) -> str:
    """Converts a type hint to its string representation.

    Args:
        type_hint: The type hint to convert.

    Returns:
        A string representation of the type hint.
    """
    origin = get_origin(type_hint)
    if origin:
        args = get_args(type_hint)
        if origin in union_like_types:
            # Process Union types, specifically checking for Optional by detecting NoneType
            non_none_args = [arg for arg in args if arg is not type(None)]
            args_str = " | ".join(get_type_hint_str(arg) for arg in non_none_args)
            return f"Optional[{args_str}]" if type(None) in args else args_str
        else:
            # Process other generic types like List, Dict
            args_str = ", ".join(get_type_hint_str(arg) for arg in args)
            return f"{origin.__name__}[{args_str}]"
    elif hasattr(type_hint, '__name__'):
        return type_hint.__name__
    else:
        return str(type_hint)