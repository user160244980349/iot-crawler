class Product:
    counter = 0

    def __new__(cls, *args, **kwargs):

        obj = {
            "id": cls.counter,
            "url": cls.is_set(kwargs, "url"),
            "manufacturer": cls.is_set(kwargs, "manufacturer"),
            "keyword": cls.is_set(kwargs, "keyword"),
            "website": cls.is_set(kwargs, "website"),
            "policy": cls.is_set(kwargs, "policy"),
            "original_policy": cls.is_set(kwargs, "original_policy"),
            "processed_policy": cls.is_set(kwargs, "processed_policy"),
            "plain_policy": cls.is_set(kwargs, "processed_policy"),
            "policy_hash": cls.is_set(kwargs, "policy_hash"),
            "statistics": cls.is_set(kwargs, "statistics"),
        }
        cls.counter += 1

        return obj

    @classmethod
    def is_set(cls, kwargs, kwarg):
        try:
            return kwargs[kwarg]

        except KeyError:
            return None
