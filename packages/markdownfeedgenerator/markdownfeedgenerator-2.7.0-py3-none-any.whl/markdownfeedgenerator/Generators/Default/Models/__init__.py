from typing import Self


class ItemStore:
    def __init__(
        self,
        initial_values: dict = None
    ):
        if initial_values:
            self.store = initial_values
        else:
            self.store = {}

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        self.store[key] = data

    def has(
        self,
        key: str
    ) -> bool:
        return key in self.store

    def has_value(
        self,
        key: str
    ) -> bool:
        """
        Check if a value exists and it is not None.
        """
        if not self.has(key):
            return False

        return self.get(key)

    def get(
        self,
        key: str
    ) -> any:
        if not self.has(key):
            available_values = list(self.store.keys())
            raise ValueError(f'Feed details store contains no value with key "{key}", values are "{available_values}".')

        return self.store[key]

    def clear(self, key=None):
        if key:
            self.store.pop(key)
        else:
            self.store = {}

    def inject(
        self,
        values_to_inject: dict
    ):
        [self.set(key, values_to_inject[key]) for key in values_to_inject]

    def merge(
        self,
        item_store: Self
    ):
        [self.set(key, item_store.get(key)) for key in item_store.store]

    def check(
        self
    ):
        pass

    def prepare_export_value(
        self,
        value: any
    ):
        if hasattr(value, 'dump') and callable(getattr(value, 'dump', None)):
            return value.dump()
        elif isinstance(value, list):
            return [self.prepare_export_value(inner_value) for inner_value in value]

        return value

    def keys(
        self
    ):
        return self.store.keys()

    def dump(
        self
    ) -> dict:
        dump = {}
        for key in self.store:
            prepared = self.prepare_export_value(self.store[key])

            if prepared is not None:
                dump[key] = prepared

        return dump

    def __iter__(
        self
    ):
        return iter(self.store.values())
