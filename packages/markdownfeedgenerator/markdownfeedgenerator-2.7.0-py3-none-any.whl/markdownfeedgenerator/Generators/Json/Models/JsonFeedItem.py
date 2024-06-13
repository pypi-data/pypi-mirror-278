from markdownfeedgenerator.Generators.Default.Models.FeedItem import FeedItem
from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore


class JsonFeedItem(FeedItem):
    """
    A class representing a JSON Feed Item.
    """

    def __init__(
        self,
        _id: str | None = None,
        url: str | None = None,
        external_url: str | None = None,
        title: str | None = None,
        content_html: str | None = None,
        content_text: str | None = None,
        summary: str | None = None,
        image: str | None = None,
        banner_image: str | None = None,
        date_published: str | None = None,
        date_modified: str | None = None,
        author: 'Author | None' = None,
        tags: [str] = None
    ):
        super().__init__()

        self.store = JsonFeedItemStore(
            ['id', 'url', 'external_url', 'title', 'content_html', 'content_text', 'summary', 'image', 'banner_image',
             'date_published', 'date_modified', 'author', 'tags'])

        # Mostly for convenience, we could also just use the store, but this makes it easier for JsonFeedItem references
        # to know exactly what can be customized.
        self.id = _id
        self.url = url
        self.external_url = external_url
        self.title = title
        self.content_html = content_html
        self.content_text = content_text
        self.summary = summary
        self.image = image
        self.banner_image = banner_image
        self.date_published = date_published
        self.date_modified = date_modified
        self.author = author
        self.tags = tags

    def set(
        self,
        key: str,
        data: any
    ) -> any:
        super().__setattr__(key, data)
        return self.store.set(key, data)

    def is_protected(
        self,
        key: str
    ) -> bool:
        """
        Check if a key is a protected (used in the JSON Feed specification) or not.
        """
        return self.store.is_protected(key)

    def __setattr__(
        self,
        key,
        value
    ):
        """
        This method is to make it convenient to use this class. It attempts to sync the store with
        the class attributes.
        """
        if hasattr(self, 'store') and hasattr(self.store, 'protected_keys') and key in self.store.protected_keys:
            self.set(key, value)

        return super().__setattr__(key, value)
