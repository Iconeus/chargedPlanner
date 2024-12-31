def singleton(cls):
    instances = {}

    class SingletonWrapper(cls):
        def __new__(inner_cls, *args, **kwargs):
            if cls not in instances:
                instances[cls] = super(SingletonWrapper, inner_cls).__new__(inner_cls, *args, **kwargs)
            return instances[cls]

    SingletonWrapper.__name__ = cls.__name__
    SingletonWrapper.__module__ = cls.__module__
    return SingletonWrapper
