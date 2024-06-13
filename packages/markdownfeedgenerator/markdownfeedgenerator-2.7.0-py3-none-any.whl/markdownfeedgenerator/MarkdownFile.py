import hashlib
import logging
import os.path
import re

import html2text
import markdown
import yaml
from dateutil import parser

from markdownfeedgenerator import read_from_file
from markdownfeedgenerator.Exceptions import DateParseError, TitleNotFoundError, InvalidMarkdownFrontMatterError


class MarkdownFile:
    """
    This class represents a single Markdown file. The markdown file should contain front-matter and contents. Please
    see https://jekyllrb.com/docs/collections/#add-content for more information.
    """

    def __init__(
        self,
        file_path: str = '',
        front_matter: dict = None,
        body: str = ''
    ):
        """
        Construct the markdown file.
        :param file_path:
        :param front_matter:
        :param body:
        """
        if not front_matter:
            front_matter = {}

        self.file_path = file_path
        self.front_matter = front_matter
        self.body = body.strip('\n')

    @property
    def file_name(
        self
    ) -> str:
        """
        Return the file name of the markdown file.
        :return:
        """
        return os.path.basename(self.file_path)

    @property
    def location(
        self
    ) -> str:
        """
        Return the location of the current file
        """
        return os.path.dirname(self.file_path)

    @property
    def filtered_front_matter(
        self
    ) -> dict:
        """
        Returns the front-matter properties with the dynamic fields such as id, title and date removed.
        """
        skip = ['id', 'title', 'date', 'summary']
        return {key: value for key, value in self.front_matter.items() if key not in skip}

    @property
    def id(
        self
    ):
        """
        Generate a unique id using the file path.
        :return:
        """
        if 'id' in self.front_matter:
            return self.front_matter['id']

        return hashlib.sha1(self.file_path.encode('utf-8')).hexdigest()

    @property
    def title(
        self
    ) -> str:
        """
        Return the title of the markdown file.
        :return:
        """
        if 'title' in self.front_matter:
            return self.front_matter['title']

        raise TitleNotFoundError('No title value was found in front-matter.')

    @property
    def date(
        self
    ):
        """
        Attempts to find the date of a file. First priority is a date value in the front-matter. If nothing is found,
        will attempt to extract from the file name. Can possibly return None if no value is found. If a date is found,
        will parse it raising a DateParseError error if/on failure.
        :return:
        """
        date = None

        if 'date' in self.front_matter:
            date = self.front_matter['date']
        else:
            date_match = re.search(r'(\d+-\d+-\d+)', self.file_name)

            if date_match:
                date = date_match[0]

        if date:
            try:
                return parser.parse(date)
            except ValueError or OverflowError:
                raise DateParseError('Unable to parse the date from the front-matter, incorrect format.')

        return date

    @property
    def html(
        self
    ) -> str:
        """
        Convert the markdown contents to html.
        :return:
        """
        return MarkdownFile.markdown_to_html(self.body)

    @property
    def summary(
        self,
        max_length: int = 100
    ) -> str:
        """
        Generate a summary of the file. If summary is in front-matter, will use that. If not, it will attempt to
        generate one from the content of the file.
        :return:
        """
        summary = self.front_matter['summary'] if 'summary' in self.front_matter else html2text.html2text(self.html)

        summary = summary.replace('\n', ' ')

        if len(summary) > max_length:
            return summary[0:max_length].strip() + '..'

        return summary.strip('\n').strip()

    @staticmethod
    def load(
        markdown_file_path: str,
        encoding: str = 'utf-8'
    ):
        """
        Load a markdown file from a file on disk.
        :param markdown_file_path:
        :param encoding:
        :return:
        """
        logging.info(f'Loading Markdown file at path "{markdown_file_path}".')

        if not os.path.exists(markdown_file_path):
            raise FileNotFoundError(f'The markdown file "{markdown_file_path}", does not exist.')

        file_segments = read_from_file(markdown_file_path, encoding).split('---', 2)

        if len(file_segments) != 3:
            raise InvalidMarkdownFrontMatterError(f'Markdown file "{markdown_file_path}" is in an incorrect format.')

        front_matter = yaml.safe_load(file_segments[1])

        if type(front_matter) is not dict:
            raise InvalidMarkdownFrontMatterError(f'Markdown file "{markdown_file_path}" has invalid front-matter.')

        return MarkdownFile(markdown_file_path, front_matter, file_segments[2])

    @staticmethod
    def markdown_to_html(
        markdown_content: str
    ) -> str:
        """
        Convert Markdown to HTML.
        """
        return markdown.markdown(markdown_content, extensions=['fenced_code', 'tables'])

    def __str__(
        self
    ):
        """
        Override for easier debugging.
        """
        if self.file_path:
            return self.file_path

        if self.title:
            return self.title

        return 'Untitled Markdown File'
