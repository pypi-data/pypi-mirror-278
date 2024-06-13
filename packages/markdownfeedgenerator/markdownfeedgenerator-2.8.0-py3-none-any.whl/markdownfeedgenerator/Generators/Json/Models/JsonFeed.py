from markdownfeedgenerator.Generators.Default.Models.Feed import Feed
from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore
from markdownfeedgenerator.Generators.Json.Models.Author import Author
from markdownfeedgenerator.Generators.Json.Models.Hub import Hub


class JsonFeed(Feed):
    """
    A class representing a JSON Feed.
    """

    def __init__(
        self,
        version: str | None = None,
        title: str | None = None,
        home_page_url: str | None = None,
        feed_url: str | None = None,
        description: str | None = None,
        user_comment: str | None = None,
        next_url: str | None = None,
        icon: str | None = None,
        fav_icon: str | None = None,
        author: Author | None = None,
        expired: bool | None = None,
        hubs: [Hub] = None
    ):
        Feed.__init__(self)

        self.store = JsonFeedItemStore(
            ['version', 'title', 'home_page_url', 'feed_url', 'description', 'feed', 'items', 'user_comment',
             'next_url', 'icon', 'fav_icon', 'author', 'expired', 'hubs'])

        self.version = version
        self.title = title
        self.home_page_url = home_page_url
        self.feed_url = feed_url
        self.description = description
        self.user_comment = user_comment
        self.next_url = next_url
        self.icon = icon
        self.fav_icon = fav_icon
        self.author = author
        self.expired = expired
        self.hubs = hubs

    def __setattr__(
        self,
        key,
        value
    ):
        if hasattr(self, 'store'):
            store = getattr(self, 'store')
            if hasattr(store, 'protected_keys') and key in store.protected_keys:
                self.set(key, value)

        return super().__setattr__(key, value)
