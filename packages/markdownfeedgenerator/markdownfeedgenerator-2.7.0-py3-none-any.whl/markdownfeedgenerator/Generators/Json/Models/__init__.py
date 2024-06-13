from markdownfeedgenerator.Generators.Default.Models import ItemStore


class JsonFeedItemStore(ItemStore):
    def __init__(
        self,
        protected_keys: list = None
    ):
        ItemStore.__init__(self)

        self.protected_keys = protected_keys if protected_keys else []

        [self.set(pk, None) for pk in self.protected_keys]

    def get(
        self,
        key: str
    ) -> any:
        if f'_{key}' in self.store:
            return self.store[f'_{key}']

        return super().get(key)

    def has(
        self,
        key: str
    ) -> any:
        if key.startswith('_'):
            key = key.lstrip('_')

        if f'_{key}' in self.store:
            return True

        return super().has(key)

    def is_protected(
        self,
        key: str
    ) -> bool:
        """
        Check if a key is in the protected key list.
        """
        return key in self.protected_keys

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        if key.startswith('_'):
            key = key.lstrip('_')

        if key in self.protected_keys:
            super().__setattr__(key, data)
            super().set(key, data)
            return

        super().set(f'_{key}', data)
