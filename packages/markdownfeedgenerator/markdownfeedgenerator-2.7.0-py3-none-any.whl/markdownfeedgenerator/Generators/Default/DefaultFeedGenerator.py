import asyncio
import json
import logging
import os
from concurrent.futures.thread import ThreadPoolExecutor
from math import ceil
from pathlib import Path
from typing import Callable

from markdownfeedgenerator.Generators import GeneratorSettings
from markdownfeedgenerator.Generators.Default.Models.Feed import Feed
from markdownfeedgenerator.Generators.Default.Models.FeedItem import FeedItem
from markdownfeedgenerator.MarkdownFile import MarkdownFile


class DefaultFeedGenerator:
    """
    Class represents a Default Feed Generator.

    This class is designed to be as "overridable" as possible, sacrificing minimal code for easy
    subclass extensibility. This class allows you to generate a paged "feed" based on Markdown files.
    """

    def __init__(
        self,
        feed: Feed = None,
        generator_settings: GeneratorSettings = None
    ):
        if not feed:
            feed_details = Feed()
            feed_details.set('title', 'Untitled Feed')

        if not generator_settings:
            generator_settings = GeneratorSettings()

        logging.info(f'Using generator with settings: "{str(generator_settings)}"')

        self.feed = feed
        self.generator_settings = generator_settings

        self._check_settings()

    async def run(
        self
    ) -> None:
        # Discover markdown file paths
        markdown_file_paths = DefaultFeedGenerator.discover_markdown_file_paths(
            self.generator_settings.get('source_directory'), self.generator_settings.get('skip_files'))

        # Last chance to process any file paths
        markdown_file_paths = self._process_file_path_list(markdown_file_paths)

        # Convert a list of file paths into a list of markdown files, async chunked work
        markdown_files = DefaultFeedGenerator.parallel_work(
            markdown_file_paths, self._process_file_path_to_markdown_file)

        # Convert a list of markdown files into a list of feed items, async chunked work
        feed_items = DefaultFeedGenerator.parallel_work(
            markdown_files, self.process_markdown_file_to_feed_item)

        # Check feed items
        self._check_feed_items(feed_items)

        # Sort the feed items
        feed_items = self._sort_feed_items(feed_items)

        # Page tracking
        current_page = 1
        feed_items_per_export = self.generator_settings.get('feed_items_per_export')
        total_pages = ceil(len(feed_items) / feed_items_per_export) if feed_items_per_export else 1

        # Convert feed items into a feed and export the feed
        exportable_feeds = []
        for chunked_feed_items in DefaultFeedGenerator.chunk(feed_items, feed_items_per_export):
            # Convert feed items into a feed
            feed = self._feed_items_to_feed(
                chunked_feed_items, current_page, total_pages, len(feed_items))

            # Check the feed is valid
            feed.check()

            logging.info(f'Successfully created feed with {len(feed.items)} items.')

            # Add feed to list of exportable feeds
            exportable_feeds.append(feed)

            current_page += 1

        # Export the completed feed
        await DefaultFeedGenerator.async_work(exportable_feeds, self._export_feed)

    def run_standalone(
        self
    ):
        """
        Run this in synchronous mode.
        """
        logging.info(f'Running feed generator in standalone mode.')
        asyncio.run(self.run())

    def _check_settings(
        self
    ):
        """
        Check the settings to ensure they contain the correct values for this generator.
        """
        pass

    def _check_feed_item(
        self,
        feed_item: FeedItem
    ):
        """
        Check if a feed item is valid or not.
        """
        logging.info(f'Checking feed item {feed_item}...')
        feed_item.check()
        
    def _check_feed_items(
        self,
        feed_items: [FeedItem]
    ):
        """
        Check feed items.
        """
        [self._check_feed_item(feed_item) for feed_item in feed_items]
        
    def _sort_feed_items(
        self,
        feed_items: [FeedItem]
    ) -> [FeedItem]:
        """
        Sort a list of feed items. Override this to provided custom sorting.
        """
        return feed_items

    def _process_markdown_file(
        self,
        markdown_file: MarkdownFile
    ) -> MarkdownFile:
        """
        Perform any needed processing on a markdown file.
        """
        return markdown_file

    def _transform_markdown_file_to_feed_item(
        self,
        markdown_file: MarkdownFile
    ) -> FeedItem:
        """
        Transform a markdown file to a feed item.
        """
        feed_item = FeedItem()
        feed_item.inject_markdown_file(markdown_file)
        return feed_item

    def process_markdown_file_to_feed_item(
        self,
        markdown_file: MarkdownFile
    ) -> FeedItem:
        """
        Process a markdown file. This function will convert a markdown file into a feed item, check its validity
        and the return it.
        """
        feed_item = self._transform_markdown_file_to_feed_item(markdown_file)

        logging.info(f'Successfully converted markdown file "{markdown_file}" to feed item.')

        return feed_item

    def _process_file_path_list(
        self,
        file_paths: list
    ) -> list:
        """
        Perform any processing on file paths.
        """
        return file_paths

    def _transform_file_path_to_markdown_file(
        self,
        file_path: str
    ) -> MarkdownFile:
        """
        Transform a file path to a markdown file.
        """
        return MarkdownFile.load(file_path)

    def _process_file_path_to_markdown_file(
        self,
        file_path: str
    ) -> MarkdownFile:
        """
        Process a file path. This function takes a file path, transforms it into a markdown file, calls a process
        function on the markdown file and then returns it.
        """
        markdown_file = self._transform_file_path_to_markdown_file(file_path)

        logging.info(f'Successfully converted file path "{file_path}" to markdown file.')

        markdown_file = self._process_markdown_file(markdown_file)

        logging.info(f'Successfully processed markdown file "{markdown_file}".')

        return markdown_file

    def _feed_items_to_feed(
        self,
        feed_items: [FeedItem],
        page: int,
        total_pages: int,
        total_items: int
    ) -> Feed:
        """
        Convert a list of feed items to a feed.
        """
        feed = self._create_feed()
        feed.page = page
        feed.items = feed_items
        feed.total_pages = total_pages
        feed.total_items = total_items
        feed.merge(self.feed)
        return feed

    def _create_feed(
        self
    ) -> Feed:
        """
        Create a new feed instance.
        """
        return Feed()

    async def _export_feed(
        self,
        feed: Feed
    ):
        """
        Export a feed.
        """
        print(json.dumps(feed.dump(), indent=2))

    @staticmethod
    def parallel_work(
        work_items: list,
        process_list_fn: Callable
    ) -> list:
        """
        This function takes a list of work items, chunks them into lists of a specified size and then
        calls a process callback function over each of those chunks. This function allows you to run chunks of work
        in parallel. The function will then await completion of all the work chunks and return the processed list.
        """
        with ThreadPoolExecutor() as ex:
            futures = [ex.submit(process_list_fn, work_item) for work_item in work_items]

        logging.info(f'Successfully completed parallel work on {len(work_items)} work items.')

        return [future.result() for future in futures]

    @staticmethod
    async def async_work(
        work_items: list,
        process_list_fn: Callable
    ) -> tuple:
        """
        Run a list of work_items through an async function process_list_fn and then await all the results, and
        then return.
        """
        futures = [process_list_fn(work_item) for work_item in work_items]

        logging.info(f'Successfully completed async work on {len(work_items)} work items.')

        return await asyncio.gather(*futures)

    @staticmethod
    def discover_markdown_file_paths(
        directory_path: str,
        skip_files: list = None
    ) -> [str]:
        """
        Discover all markdown files within a provided directory, skipping some files if needed.
        """
        if skip_files is None:
            skip_files = []

        if not os.path.isdir(directory_path):
            raise Exception(f'The provided path "{directory_path}", must be a directory.')

        return list(
            filter(
                lambda x: os.path.basename(x) not in skip_files,
                [str(path) for path in Path(directory_path).glob('**/*.md')]))

    @staticmethod
    def chunk(
        items: list,
        length: int = None
    ) -> list:
        """
        Chunk a list into a specific length. If no length is provided, just yield the original list.
        """
        if length is None:
            yield items
            return

        for i in range(0, len(items), length):
            yield items[i:i + length]
