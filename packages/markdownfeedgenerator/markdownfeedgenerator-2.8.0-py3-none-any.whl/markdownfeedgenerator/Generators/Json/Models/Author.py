from markdownfeedgenerator.Generators.Default.Exceptions import InvalidFeedItemValueError
from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore
from markdownfeedgenerator.Generators.Json.Models.JsonFeedItem import JsonFeedItem


class Author(JsonFeedItem):
    """
    A class representing a JSON Feed Author.
    """

    def __init__(
        self,
        name: str = None,
        url: str = None,
        avatar: str = None
    ):
        super().__init__()

        self.store = JsonFeedItemStore(['name', 'url', 'avatar'])

        self.name = name
        self.url = url
        self.avatar = avatar

    def check(
        self
    ):
        if not self.has_value('name') and not self.has_value('url') and not self.has_value('avatar'):
            raise InvalidFeedItemValueError(
                'You must provide a value for at least one of the "name", "url" or "avatar" properties.')

        super().check()
