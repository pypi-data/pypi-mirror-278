import json
import os


class GeneratorSettings:
    def __init__(
        self,
        feed_items_per_export: int = 100,
        source_directory: str = None,
        target_directory: str = None,
        skip_files: list = None,
        **kwargs
    ):
        self.settings = {}

        # Set some common settings manually
        self.set('feed_items_per_export', feed_items_per_export)
        self.set('source_directory', source_directory.rstrip(os.sep) if source_directory else None)
        self.set('target_directory', target_directory.rstrip(os.sep) if target_directory else None)
        self.set('skip_files', skip_files if skip_files else [])

        # All other settings
        [self.set(key, kwargs[key]) for key in kwargs]

    def get(
        self,
        key
    ) -> any:
        return self.settings[key]

    def has(
        self,
        key
    ) -> bool:
        return key in self.settings

    def set(
        self,
        key,
        value
    ):
        self.settings[key] = value

    def check(
        self
    ):
        pass

    def __str__(
        self
    ):
        return json.dumps(self.settings)
