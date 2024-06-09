import unittest
from http import HTTPStatus

import httpx
from parameterized import parameterized

from sitemappy.link_scraper import AsyncScraper


class TestLinkScraper(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def __generate_html_page_of_links(links: list[str]) -> str:
        html_links = [f"<a href={link}>{index}</a>" for index, link in enumerate(links)]
        return f"<html>{html_links}</html>"

    async def test_successful_get_links(self) -> None:
        # Arrange
        expected_response = [
            "https://monzo.com/careers",
            "https://monzo.com/about",
        ]
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    HTTPStatus.OK,
                    content=self.__generate_html_page_of_links(expected_response),
                )
            )
        )

        class_under_test = AsyncScraper("https://monzo.com", client=client)

        # Act
        response = await class_under_test.get_links(class_under_test.base_url)

        # Assert
        self.assertEqual(expected_response, response)

    @parameterized.expand(
        [
            (
                "https://monzo.com",
                [
                    "https://monzo.com#careers",
                    "https://monzo.com/business-banking",
                ],
                ["#careers", "/business-banking"],
            ),
            (
                "https://www.monzo.com/",
                [
                    "https://www.monzo.com/#careers",
                    "https://www.monzo.com/business-banking",
                ],
                ["#careers", "/business-banking"],
            ),
        ]
    )  # type: ignore[misc]
    async def test_successful_get_relative_url(
        self, base_url: str, expected_urls: list[str], relative_urls: list[str]
    ) -> None:
        # Arrange
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    HTTPStatus.OK,
                    content=self.__generate_html_page_of_links(relative_urls),
                )
            )
        )

        class_under_test = AsyncScraper(base_url, client=client)

        # Act
        response = await class_under_test.get_links(class_under_test.base_url)

        # Assert
        self.assertEqual(expected_urls, response)

    async def test_unsuccessful_get_url(self) -> None:
        # Arrange
        expected_number_of_links = 0
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(HTTPStatus.INTERNAL_SERVER_ERROR)
            )
        )

        class_under_test = AsyncScraper("https://monzo.com", client=client)

        # Act
        response = await class_under_test.get_links(class_under_test.base_url)

        # Assert
        self.assertEqual(expected_number_of_links, len(response))

    @parameterized.expand(  # type: ignore[misc]
        [
            # (Base URL, Test URL)
            ("https://monzo.com", "https://monzo.com/"),  # Appended empty "/" path
            ("https://monzo.com", "https://monzo.com/careers"),  # Appended path
            (
                "https://monzo.com",
                "https://monzo.com/#business",
            ),  # Appended anchor link to empty "/" path
            (
                "https://community.monzo.com",
                "https://community.monzo.com/profile",
            ),  # Appended path with subdomain
        ]
    )
    def test_link_is_in_same_subdomain(self, base_url: str, test_url: str) -> None:
        # Arrange
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(HTTPStatus.INTERNAL_SERVER_ERROR)
            )
        )

        class_under_test = AsyncScraper(base_url, client=client)

        # Act
        response = class_under_test.is_in_same_subdomain(test_url)

        # Assert
        self.assertTrue(response)

    @parameterized.expand(  # type: ignore[misc]
        [
            # (Base URL, Test URL)
            ("https://monzo.com", "https://monzo.commalformedurl"),  # Malformed URL
            ("https://monzo.com", "https://community.monzo.com"),  # Appended subdomain
            ("https://community.monzo.com", "https://monzo.com"),  # Missing subdomain
            ("https://www.monzo.com", "https://monzo.com"),  # Appended "www" subdomain
            ("https://facebook.com", "https://monzo.com"),  # Different domain name
            ("https://monzo.co.uk", "https://monzo.com"),  # Different TLD
            (
                "https://monzo.com",
                "https://monzo.com#careers",
            ),  # Appended anchor link, no path
        ]
    )
    def test_link_is_not_in_same_subdomain(self, base_url: str, test_url: str) -> None:
        # Arrange
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(HTTPStatus.INTERNAL_SERVER_ERROR)
            )
        )

        class_under_test = AsyncScraper(base_url, client=client)

        # Act
        response = class_under_test.is_in_same_subdomain(test_url)

        # Assert
        self.assertFalse(response)
