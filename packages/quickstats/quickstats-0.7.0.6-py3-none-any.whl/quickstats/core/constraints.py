class BaseConstraint:
    def __call__(self, obj):
        return True

    def __repr__(self):
        className = self.__class__.__name__
        attributes = ", ".join(f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith('_'))
        return f"{className}({attributes})"

    def __eq__(self):
        return type(self) == type(other)

class RangeConstraint(BaseConstraint):
    """
    Restricts the range of an object
    """
    def __init__(self, vmin, vmax, lbound=True, rbound=True):
        """
        Args:
            vmin: Minimum value of the range.
            vmax: Maximum value of the range.
            lbound: If True, vmin is inclusive. Defaults to True.
            rbound: If True, vmax is inclusive. Defaults to True.        
        """
        if vmin > vmax:
            raise ValueError("vmin must be less than or equal to vmax")
        if not isinstance(lbound, bool) or not isinstance(rbound, bool):
            raise ValueError("lbound and rbound must be boolean values")
        
        self.vmin = vmin
        self.vmax = vmax
        self.lbound = lbound
        self.rbound = rbound
        self._lopt = '__le__' if lbound else '__lt__'
        self._ropt = '__ge__' if rbound else '__gt__'

    def __call__(self, obj):
        if not hasattr(obj, self._lopt) or not hasattr(obj, self._ropt):
            raise ValueError(f"{obj} does not support '{self._lopt}' and '{self._ropt}', required for this range constraint.")
        
        lopt_result = getattr(obj, self._lopt)(self.vmin)
        ropt_result = getattr(obj, self._ropt)(self.vmax)
        return lopt_result and ropt_result

    def __eq__(self, other):
        if not isinstance(other, RangeConstraint):
            return False
        return (self.vmin, self.vmax, self.lbound, self.rbound) == (other.vmin, other.vmax, other.lbound, other.rbound)

class MinConstraint(BaseConstraint):
    """
    Restricts the minimum value of an object
    """
    def __init__(self, vmin, inclusive=True):
        """
        Args:
            vmin: The minimum allowable value.
            inclusive: If True, vmin is included in the valid range. Defaults to True.        
        """
        if not isinstance(inclusive, bool):
            raise ValueError("inclusive must be a boolean value")
        
        self.vmin = vmin
        self.inclusive = inclusive
        self._opt = '__le__' if inclusive else '__lt__'

    def __call__(self, obj):
        if not hasattr(obj, self._opt):
            raise ValueError(f"{obj} does not support the '{self._opt}' comparison operator required for this minimum constraint.")
        
        return getattr(obj, self._opt)(self.vmin)

    def __eq__(self, other):
        if not isinstance(other, MinConstraint):
            return False
        return (self.vmin, self.inclusive) == (other.vmin, other.inclusive)


class MaxConstraint(BaseConstraint):
    """
    Restricts the maximum value of an object
    """
    def __init__(self, vmax, inclusive=True):
        """
        Args:
            vmax: The maximum allowable value.
            inclusive: If True, vmax is included in the valid range. Defaults to True.
        """
        if not isinstance(inclusive, bool):
            raise ValueError("inclusive must be a boolean value")
        
        self.vmax = vmax
        self.inclusive = inclusive
        self._opt = '__ge__' if inclusive else '__gt__'

    def __call__(self, obj):
        if not hasattr(obj, self._opt):
            raise ValueError(f"{obj} does not support the '{self._opt}' comparison operator required for this maximum constraint.")
        
        return getattr(obj, self._opt)(self.vmax)

    def __eq__(self, other):
        if not isinstance(other, MaxConstraint):
            return False
        return (self.vmax, self.inclusive) == (other.vmax, other.inclusive)


class ChoiceConstraint(BaseConstraint):
    """
    Restricts the value of an object to be among a given set of choices
    """
    def __init__(self, *choices):
        """
        Args:
            *choices: A variable-length list of allowable choices.
        """
        self.choices = set(choices)

    def __call__(self, obj):
        if obj not in self.choices:
            raise ValueError(f"{obj} is not one of the allowed choices: {self.choices}")
        return True

    def __eq__(self, other):
        if not isinstance(other, ChoiceConstraint):
            return False
        # Note: Direct set comparison
        return self.choices == other.choices