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
        return super().get(self.get_key_name(key))

    def clear(self, key=None):
        super().clear(self.get_key_name(key))

    def has(
        self,
        key: str
    ) -> any:
        return super().has(self.get_key_name(key))

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        key = self.get_key_name(key)

        if key in self.protected_keys:
            super().__setattr__(key, data)
            super().set(key, data)
            return

        super().set(key, data)

    def is_protected(
        self,
        key: str
    ) -> bool:
        """
        Check if a key is in the protected key list.
        """
        return key in self.protected_keys

    def get_key_name(
        self,
        key: str
    ) -> str:
        """
        Get a protected key name.
        """
        if key.startswith('_'):
            key = key.lstrip('_')

        if key in self.protected_keys:
            return key

        return f'_{key}'
