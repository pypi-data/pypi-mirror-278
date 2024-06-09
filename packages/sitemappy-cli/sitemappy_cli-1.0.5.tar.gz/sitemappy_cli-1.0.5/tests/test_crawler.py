import unittest
from unittest import mock
from unittest.mock import AsyncMock, Mock, call, patch

from parameterized import parameterized

from sitemappy.crawler import (
    DEFAULT_NUMBER_OF_WORKERS,
    POLITENESS_DELAY_DEFAULT_S,
    UNLIMITED_DEPTH,
    Crawler,
)


@mock.patch("sitemappy.crawler.AsyncScraper.get_links", new_callable=AsyncMock)
@patch("sitemappy.crawler.time.sleep")
class TestCrawler(unittest.IsolatedAsyncioTestCase):
    @parameterized.expand(  # type: ignore[misc]
        [
            # Base URL, Links to Return
            ("https://monzo.com", []),
            ("https://monzo.com", ["+442038720620"]),
            ("https://monzo.com", ["mailto:careers@monzo.com"]),
            ("https://monzo.com", ["https://monzo.commalformedurl"]),
            ("https://monzo.com", ["+442038720620", "mailto:careers@monzo.com"]),
        ]
    )
    async def test_base_url_crawl_links(
        self,
        mock_sleep: Mock,
        mock_scraper_get_links: AsyncMock,
        base_url: str,
        links_to_return: list[str],
    ) -> None:
        # Arrange
        expected = {
            base_url: links_to_return,
        }
        mock_scraper_get_links.return_value = links_to_return

        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_sleep.assert_not_called()
        self.assertEqual(DEFAULT_NUMBER_OF_WORKERS, crawler.number_of_workers)
        self.assertEqual(UNLIMITED_DEPTH, crawler.crawl_depth)
        self.assertEqual(POLITENESS_DELAY_DEFAULT_S, crawler.politeness_delay)

        mock_scraper_get_links.assert_called_once()
        self.assertDictEqual(expected, results)

    async def test_base_url_with_relative_links(
        self,
        _: Mock,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/test"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
            second_crawl_url: subdomain_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls(
            [call(base_url), call(second_crawl_url)]
        )
        self.assertDictEqual(expected, results)

    async def test_crawl_depth_less_than_one(
        self,
        _: Mock,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/test"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
            second_crawl_url: subdomain_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls(
            [call(base_url), call(second_crawl_url)]
        )
        self.assertDictEqual(expected, results)

    async def test_crawl_depth_one_only_crawls_single_page(
        self,
        _: Mock,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        crawl_depth = 1
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/careers"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url, crawl_depth=crawl_depth)

        # Act
        results = await crawler.crawl()

        # Assert
        # Only called once due to depth set to 1
        mock_scraper_get_links.assert_has_calls([call(base_url)])
        self.assertDictEqual(expected, results)

    async def test_politeness_delay_less_than_one(
        self,
        mock_sleep: Mock,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        politeness_delay = -1
        base_url = "https://monzo.com"
        base_url_links = ["mailto:careers@monzo.com"]

        expected = {
            base_url: base_url_links,
        }

        mock_scraper_get_links.return_value = base_url_links
        crawler = Crawler(base_url, politeness_delay=politeness_delay)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls([call(base_url)])
        mock_sleep.assert_not_called()
        self.assertDictEqual(expected, results)

    async def test_politeness_delay_causes_thread_sleep(
        self,
        mock_sleep: Mock,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        politeness_delay = 99
        base_url = "https://monzo.com"
        base_url_links = ["mailto:careers@monzo.com"]

        expected = {
            base_url: base_url_links,
        }

        mock_scraper_get_links.return_value = base_url_links
        crawler = Crawler(base_url, politeness_delay=politeness_delay)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls([call(base_url)])
        mock_sleep.assert_has_calls([call(politeness_delay)])
        self.assertDictEqual(expected, results)
