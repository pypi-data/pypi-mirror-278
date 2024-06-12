
def get_full_class_name(str_cls_or_obj: str | type | object) -> str:
    """Get the full class name of a class or object.
    Args:
        str_cls_or_obj (str | type | object): The string or class or object.
    Returns:
        str: The full class name.
    """
    if isinstance(str_cls_or_obj, str):
        return str_cls_or_obj
    cls = str_cls_or_obj if isinstance(str_cls_or_obj, type) else str_cls_or_obj.__class__
    module = cls.__module__
    name = cls.__qualname__
    if module is None or module == str.__class__.__module__:
        return name  # Avoid reporting __builtin__
    return module + "." + name