def dynamic_import(obj_path):
    """
    Return an object foo given an object path:
    bar.foo
    """

    components = obj_path.split('.')
    mod = __import__(components[0])

    for comp in components[1:]:

        try:
            mod = getattr(mod, comp)
        except AttributeError, e:
            print e
            raise ImportError
    return mod
