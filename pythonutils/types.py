def get_class_name(inst):
    cls = getattr(inst, '__class__', inst)
    return cls.__name__
