class Product:
    counter = 0

    def __new__(cls, *args, **kwargs):
        obj = {
            "id": cls.counter,
            "url": None,
            "manufacturer": None,
            "keyword": None,
            "website": None,
            "policy": None,
            "original_policy": None,
            "processed_policy": None,
            "plain_policy": None,
            "policy_hash": None,
            "statistics": None,
        }
        cls.counter += 1

        return {**obj, **kwargs}
