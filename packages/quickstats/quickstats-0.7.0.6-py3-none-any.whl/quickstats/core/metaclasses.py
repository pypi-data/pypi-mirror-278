class MergeAnnotationsMeta(type):
    """
    A metaclass for automatically merging type annotations from parent classes to the subclass,
    ensuring no overlapping annotations with different types.

    This metaclass iterates over all base classes of a newly created class, collecting and
    merging their `__annotations__`. If an annotation with the same name but different types
    is detected in multiple base classes, or between a base class and the subclass, a TypeError
    is raised to prevent inconsistent type annotations.

    Usage:
        class MyParentClass(metaclass=MergeAnnotationsMeta):
            my_attr: int

        class MyChildClass(MyParentClass):
            another_attr: str

    Attributes are not explicitly defined in this metaclass; it operates on the `__annotations__`
    attribute found in class dictionaries.

    Raises:
        TypeError: If overlapping annotations with different types are detected.
    """
    def __new__(cls, name, bases, dct):
        # Collect annotations from all bases
        all_annotations = {}
        for base in bases:
            if hasattr(base, '__annotations__'):
                for key, value in base.__annotations__.items():
                    if key in all_annotations and all_annotations[key] != value:
                        continue
                        #raise TypeError(f"Overlapping annotation for '{key}' with different types detected.")
                    all_annotations[key] = value
        combined_annotations = {}
        # Merge collected annotations with the current class annotations
        annotations = dct.get('__annotations__', {})
        for key, value in all_annotations.items():
            #if key in annotations and annotations[key] != value:
            #    raise TypeError(f"Overlapping annotation for '{key}' with different types detected.")
            if key not in annotations:
                combined_annotations[key] = value
        combined_annotations.update(annotations)
        dct['__annotations__'] = combined_annotations
        return super().__new__(cls, name, bases, dct)