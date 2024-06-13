from typing import Self

from markdownfeedgenerator.Generators.Default.Models import ItemStore
from markdownfeedgenerator.Generators.Default.Models.FeedItem import FeedItem


class Feed:
    def __init__(
        self
    ):
        self.store = ItemStore()

        self.items: [FeedItem] = []
        self.page = None
        self.total_pages = None
        self.total_items = None

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        self.store.set(key, data)

    def has(
        self,
        key: str
    ) -> bool:
        return self.store.has(key)

    def get(
        self,
        key: str
    ) -> any:
        return self.store.get(key)

    def inject(
        self,
        values_to_inject: dict
    ):
        for key in values_to_inject:
            self.store.set(key, values_to_inject[key])

    def merge(
        self,
        item_store: Self
    ):
        self.inject(item_store.dump())

    def check(
        self
    ):
        self.store.check()

    def dump(
        self
    ) -> dict:
        self.store.set('items', self.items)
        self.store.set('page', self.page)
        self.store.set('total_pages', self.total_pages)
        self.store.set('total_items', self.total_pages)

        return self.store.dump()
