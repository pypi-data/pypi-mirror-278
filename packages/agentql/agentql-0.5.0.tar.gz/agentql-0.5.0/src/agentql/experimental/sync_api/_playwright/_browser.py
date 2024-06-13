from typing import List

from playwright.sync_api import Browser, StorageState, sync_playwright, BrowserContext

from agentql.experimental.sync_api._protocol._browser import Browser as BrowserProtocol
from agentql.experimental.sync_api._playwright._page._main import PlaywrightPage
from agentql._core._errors import OpenUrlError


class Playwright(BrowserProtocol[PlaywrightPage, Browser, BrowserContext]):
    """
    An implementation of Browser protocol using Playwright SDK. Represents a browser which handles multiple pages.
    """

    def __init__(self, browser: Browser, context: BrowserContext):
        self.browser = browser
        self.context = context

    @classmethod
    def chromium(
        cls,
        headless: bool = True,
        user_auth_session: StorageState | None = None,
        user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    ) -> "Playwright":
        """
        Initialize a standard Playwright chromium browser.

        Parameters:
        -----------
        headless (bool) (optional): Run browser in a headless mode.
        user_auth_session (StorageState) (optional): Specify a snapshot of user data such as cookies, auth sessions.
        user_agent (str) (optional): Specify a user-agent applied to the browser.
        """
        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(headless=headless)

        context = browser.new_context(storage_state=user_auth_session, user_agent=user_agent)

        return cls(browser, context)

    @classmethod
    def from_cdp(cls, url: str) -> "Playwright":
        """
        Connect to an existing browser using Chrome DevTools Protocol.

        Parameters:
        -----------
        url (str): Url to connect.
        """
        playwright = sync_playwright().start()

        browser = playwright.chromium.connect_over_cdp(url)

        context = browser.contexts[0]

        return cls(browser, context)

    def stop(self):
        """
        Stop the browser and close all pages associated with it.
        """
        self.browser.close()

    @property
    def pages(self) -> List[PlaywrightPage]:
        """
        A list of pages which browser has (in default context).

        Returns:
        --------
        list[PageImplementation]: A list of Page implementation objects which represent pages.
        """
        return [PlaywrightPage(page) for page in self.context.pages]

    def open(self, url: str | None = None) -> PlaywrightPage:
        """
        Creates a new tab instance, and optionally opens a new url.

        Returns:
        --------
        PageImplementation: A newly created page via Page implementation object.
        """
        try:
            page = self.context.new_page()

            if url:
                page.goto(url)

        except Exception as exc:
            raise OpenUrlError(url) from exc

        return PlaywrightPage(page)
