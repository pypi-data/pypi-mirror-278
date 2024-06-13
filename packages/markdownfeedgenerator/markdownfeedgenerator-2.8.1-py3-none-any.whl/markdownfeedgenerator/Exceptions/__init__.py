class DateParseError(ValueError):
    """
    An error when parsing a date.
    """
    pass


class TitleNotFoundError(TypeError):
    """
    An error when a title has not been found.
    """
    pass


class InvalidMarkdownFrontMatterError(ValueError):
    """
    An error when a markdown file has invalid front matter.
    """
    pass
