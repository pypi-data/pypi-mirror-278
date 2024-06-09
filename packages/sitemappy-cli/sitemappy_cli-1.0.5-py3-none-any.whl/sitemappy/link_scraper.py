from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

HTTP_TRANSPORTS = ["http://", "https://"]


class AsyncScraper:
    """
    An asynchronous scraper to get all links for a given webpage.
    """

    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient | None = None,
    ):
        """
        Initialise a new asynchronous link scaper.

        :param base_url: Base URL of the site to crawl
        :param client: httpx.AsyncClient for making requests
        """
        self.base_url = base_url
        self.parsed_base_url = urlparse(base_url)
        self.client = client if client else httpx.AsyncClient()

    async def get_links(self, url: str) -> list[str]:
        """
        Get all links present on a webpage.

        :param url: The URL of the webpage to scrape
        :return: List of URLs referenced on the page
        """
        links = []

        page = await self.client.get(url=url)
        soup = BeautifulSoup(page.text, "html.parser")

        for html_link_element in soup.find_all("a"):
            link: str = html_link_element.get("href")

            if link:
                if not any(link.startswith(prefix) for prefix in HTTP_TRANSPORTS):
                    # If the link does not start with the HTTP transport, it must be
                    # a relative path so append the base URL.
                    link = urljoin(self.base_url, link)

                links.append(link)

        return links

    def is_in_same_subdomain(self, link: str) -> bool:
        """
        Identify if a link/URL is part of the subdomain being scraped.

        :param link: Link to check
        :return: Boolean value indicating the link is part of the configured
            AsyncScraper.base_url
        """
        return any(
            link.startswith(f"{prefix}{self.parsed_base_url.hostname}/")
            for prefix in HTTP_TRANSPORTS
        )
