import asyncio
import json
import time

from .link_scraper import AsyncScraper

HTTP_TRANSPORTS = ["http://", "https://"]

POLITENESS_DELAY_DEFAULT_S = 0

UNLIMITED_DEPTH = 0
STARTING_DEPTH = 0

DEFAULT_NUMBER_OF_WORKERS = 10


class Crawler:
    """
    A Crawler to spin up a set of workers running through Queue items until complete.
    """

    def __init__(  # noqa: PLR0913 - Could move to Pydantic models in the future
        self,
        base_url: str,
        number_of_workers: int = DEFAULT_NUMBER_OF_WORKERS,
        crawl_depth: int = UNLIMITED_DEPTH,
        politeness_delay: int = POLITENESS_DELAY_DEFAULT_S,
        enable_cmd_out: bool = False,
    ):
        """
        Initialise a new Crawler with asynchronous scraper.

        :param base_url: Website to crawl

        :param number_of_workers: Workers to concurrently crawl pages for links
            *(default: 10)*

        :param crawl_depth: Depth of links from base URL to follow
            *(default: 0 - unlimited)*

        :param politeness_delay: Delay between each request
            *(default: 0 - no delay)*
        """
        self.number_of_workers = number_of_workers
        self.crawl_depth = crawl_depth
        self.politeness_delay = politeness_delay
        self.enable_cmd_out = enable_cmd_out

        self.scraper = AsyncScraper(base_url)

        self._crawl_queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
        self._results: dict[str, list[str]] = {}
        self._crawled_urls: set[str] = set()

    async def _worker(self) -> None:
        while True:
            # Get next item from queue and current depth
            page_to_crawl, depth = await self._crawl_queue.get()

            # If the page has already been crawled,
            # or crawl depth is configured and has been reached
            if page_to_crawl in self._crawled_urls or (
                UNLIMITED_DEPTH < self.crawl_depth <= depth
            ):
                self._crawl_queue.task_done()
                continue

            # Add to list of crawled URLs if not already been crawled
            self._crawled_urls.add(page_to_crawl)

            # If the politeness delay is configured, delay between each
            # request across threads
            if self.politeness_delay > POLITENESS_DELAY_DEFAULT_S:
                time.sleep(self.politeness_delay)

            links = await self.scraper.get_links(page_to_crawl)

            for link in links:
                if self.scraper.is_in_same_subdomain(link):
                    # If retrieved link is in the same subdomain, set
                    # depth and add to the queue
                    new_depth = depth + 1
                    await self._crawl_queue.put((link, new_depth))

            # Add to dictionary of results, using Set separately to avoid
            # race conditions across async tasks
            self.cmd_out(json.dumps({page_to_crawl: links}))
            self._results[page_to_crawl] = links
            self._crawl_queue.task_done()

    async def crawl(self) -> dict[str, list[str]]:
        """
        Start async workers crawling through website, starting from the
        Crawler.base_url.

        :return: *dict[str, list[str]]* - Map of pages that have been crawled and links
            gathered from that page.
        """
        self._crawl_queue.put_nowait((self.scraper.base_url, STARTING_DEPTH))

        workers = [
            asyncio.create_task(self._worker()) for _ in range(self.number_of_workers)
        ]

        await self._crawl_queue.join()

        for worker in workers:
            worker.cancel()

        return self._results

    def cmd_out(self, msg: str) -> None:
        """
        If cmd output is enabled, print message.

        :param msg: Message to print
        :return:
        """
        if self.enable_cmd_out:
            print(msg)
