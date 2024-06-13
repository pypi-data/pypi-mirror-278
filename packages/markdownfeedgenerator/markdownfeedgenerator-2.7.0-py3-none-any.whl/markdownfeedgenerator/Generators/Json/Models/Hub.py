from markdownfeedgenerator.Generators.Default.Exceptions import InvalidFeedItemValueError
from markdownfeedgenerator.Generators.Json.Models import JsonFeedItemStore
from markdownfeedgenerator.Generators.Json.Models.JsonFeedItem import JsonFeedItem


class Hub(JsonFeedItem):
    """
    A class representing a JSON Feed Hub.
    """

    def __init__(
        self,
        hub_type: str = None,
        url: str = None
    ):
        super().__init__()
        self.store = JsonFeedItemStore(['type', 'url'])

        self.type = hub_type
        self.url = url

    def check(
        self
    ):
        if not self.has_value('type') or not self.has_value('url'):
            raise InvalidFeedItemValueError('You must provide a valid value for both "type" and "url".')

        super().check()
