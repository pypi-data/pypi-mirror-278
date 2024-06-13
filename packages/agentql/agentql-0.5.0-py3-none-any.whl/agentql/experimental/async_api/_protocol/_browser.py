from typing import TypeVar, Protocol

from agentql.experimental.async_api._protocol._page import Page


PageImplementation = TypeVar("PageImplementation", bound=Page)
BrowserTypeT = TypeVar("BrowserTypeT")
ContextTypeT = TypeVar("ContextTypeT")


class Browser(Protocol[PageImplementation, BrowserTypeT, ContextTypeT]):
    """
    The Browser protocol represents an async implementation of browser (session) which works with multiple pages.
    """

    browser: BrowserTypeT
    """A driver-specific browser interface, assigned during __init__."""

    context: ContextTypeT
    """A driver-specific context interface (assigned internally)."""

    async def close(self):
        """
        Stops the browser and closes all pages associated with it.
        """

    @property
    def pages(self) -> list[PageImplementation]:
        """
        A list of pages which browser has (in default context).

        Returns:
        --------
        list[PageImplementation]: A list of Page implementation objects which represent pages.
        """
        raise NotImplementedError()

    async def open(self, url: str | None = None) -> PageImplementation:
        """
        Creates a new tab instance, and optionally opens a new url.

        Returns:
        --------
        PageImplementation: A newly created page via Page implementation object.
        """
        raise NotImplementedError()
