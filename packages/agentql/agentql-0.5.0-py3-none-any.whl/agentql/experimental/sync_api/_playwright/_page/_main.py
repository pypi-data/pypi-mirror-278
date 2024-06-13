import time
import logging

from playwright.sync_api import Error

from agentql import QueryParser, trail_logger
from agentql._core._errors import (
    PageMonitorNotInitializedError,
    UnableToClosePopupError,
    AccessibilityTreeError,
    AttributeNotFoundError,
    ElementNotFoundError,
    AgentQLServerError,
    OpenUrlError,
)

from agentql.experimental.sync_api._protocol._page import Page as PageProtocol
from agentql.experimental.sync_api._response_proxy import AQLResponseProxy
from agentql.ext.playwright._utils import post_process_accessibility_tree
from agentql.ext.playwright._network_monitor import PageActivityMonitor
from agentql.sync_api._agentql_service import query_agentql_server
from agentql._core._js_snippets.snippet_loader import load_js
from agentql.experimental.sync_api._query import Query

from agentql.ext.playwright.sync_api.playwright_driver_sync import (
    get_page_accessibility_tree,
    find_element_by_id,
    process_iframes,
    Locator,
    Page,
)

log = logging.getLogger("agentql")


class PlaywrightPage(
    PageProtocol[Locator, Page], Query[Locator, Page]
):  # Figure out later it's mischevous MRO complaining behavior.

    def __init__(self, page: Page, check_popup: bool = False):
        self.page = page
        """Original Page object by Playwright driver."""

        self._check_popup = check_popup
        self._event_listeners = {}
        self._page_monitor = None
        self._original_html = None
        self._last_accessibility_tree = None

    def __str__(self) -> str:
        return f"<Page url={self.page.url}>"

    def __repr__(self) -> str:
        return f"<Page url={self.page.url}>"

    @property
    def _accessibility_tree(self) -> dict:
        try:
            accessibility_tree = get_page_accessibility_tree(self.page)
            process_iframes(self.page, accessibility_tree)
            return accessibility_tree

        except Exception as e:
            raise AccessibilityTreeError() from e

    @property
    def url(self) -> str:
        return self.page.url

    def open(self, url: str):  # TODO EXCEPTION HANDLING!
        """Opens a new url in a page."""
        try:
            self.page.goto(url)

        except Exception as exc:
            raise OpenUrlError(url) from exc

    def close(self):
        self.page.close()

    def _prepare_accessibility_tree(self, include_aria_hidden: bool) -> dict:
        self._original_html = self.page.content()

        try:
            accessibility_tree = get_page_accessibility_tree(
                self.page, include_aria_hidden=include_aria_hidden
            )
            process_iframes(self.page, accessibility_tree)
            post_process_accessibility_tree(accessibility_tree)
            return accessibility_tree

        except Exception as e:
            raise AccessibilityTreeError() from e

    def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        trail_logger.add_event(f"Waiting for {self.page} to reach 'Page Ready' state")

        if not self._page_monitor:
            self._page_monitor = PageActivityMonitor()
        else:
            # Reset the network monitor to clear the logs
            self._page_monitor.reset()

        # Add event listeners to track DOM changes and network activities
        self._add_event_listeners_for_page_monitor(self.page)

        # Wait for the page to reach the "Page Ready" state
        self._determine_load_state(
            self.page, self._page_monitor, wait_for_network_idle=wait_for_network_idle
        )

        # Remove the event listeners to prevent overwhelming the async event loop
        self._remove_event_listeners_for_page_monitor(self.page)

        trail_logger.add_event(f"Finished waiting for {self.page} to reach 'Page Ready' state")

    def _locate_interactive_element(self, response_data: dict) -> Locator:
        tf623_id = response_data.get("tf623_id")
        if not tf623_id:
            raise ElementNotFoundError(self.page.url, "tf623_id")
        iframe_path = response_data.get("attributes", {}).get("iframe_path")
        interactive_element = find_element_by_id(
            page=self.page, tf623_id=tf623_id, iframe_path=iframe_path
        )
        trail_logger.spy_on_object(interactive_element)
        return interactive_element

    def _determine_load_state(
        self,
        page: Page,
        monitor: PageActivityMonitor,
        timeout_seconds: int = 14,
        wait_for_network_idle: bool = True,
    ):
        if not self._page_monitor:
            raise PageMonitorNotInitializedError()

        start_time = time.time()

        while True:
            if wait_for_network_idle:
                try:
                    last_updated_timestamp = page.evaluate(load_js("get_last_dom_change"))
                # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
                except Error:
                    while True:
                        if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                            break
                        time.sleep(0.2)
                    # monitor.check_conditions() is expecting milliseconds
                    last_updated_timestamp = time.time() * 1000

                if monitor.is_page_ready(last_active_dom_time=last_updated_timestamp):
                    break
            else:
                if self._page_monitor.get_load_status():
                    trail_logger.add_event("Page ready: Page emitted 'load' event.")
                    break

            if time.time() - start_time > timeout_seconds:
                trail_logger.add_event("Page ready: Timeout while waiting for page to settle.")
                break
            time.sleep(0.1)

    def _add_event_listeners_for_page_monitor(self, page: Page):
        if not self._page_monitor:
            raise PageMonitorNotInitializedError()

        try:
            page.on("request", self._page_monitor.track_network_request)
            page.on("requestfinished", self._page_monitor.track_network_response)
            page.on("requestfailed", self._page_monitor.track_network_response)
            page.on("load", self._page_monitor.track_load)
            page.evaluate(load_js("add_dom_change_listener"))
        # If the page is navigating, the evaluate function will raise an error. In this case, we wait for the page to load.
        except Error:
            start_time = time.time()
            while True:
                if self._page_monitor.get_load_status() or time.time() - start_time > 6:
                    break
                time.sleep(0.2)

    def _remove_event_listeners_for_page_monitor(self, page: Page):
        if not self._page_monitor:
            raise PageMonitorNotInitializedError()

        try:
            page.remove_listener("request", self._page_monitor.track_network_request)
            page.remove_listener("requestfinished", self._page_monitor.track_network_response)
            page.remove_listener("requestfailed", self._page_monitor.track_network_response)
            page.remove_listener("load", self._page_monitor.track_load)
            page.evaluate(load_js("remove_dom_change_listener"))
        except Error:
            log.warning("Unable to remove event listeners for page monitor.")

    def _find_element_by_id(self, tf623_id: str, iframe_path: str = "") -> Locator:
        try:
            element_frame_context = self._get_frame_context(iframe_path)
            return element_frame_context.locator(f"[tf623_id='{tf623_id}']")
        except Exception as e:
            raise ElementNotFoundError(self.page.url, tf623_id) from e

    def _get_text_content(self, web_element: Locator) -> str | None:
        return web_element.text_content()

    def _close_popup(self, popup_tree: dict, page_url: str, timeout: int = 500):
        query = """
            {
                popup {
                    close_btn
                }
            }
        """
        parser = QueryParser(query)
        query_tree = parser.parse()
        try:
            response = query_agentql_server(query, popup_tree, timeout=timeout, page_url=page_url)
            agentql_response = AQLResponseProxy(response, self, query_tree)
            agentql_response.popup.close_btn.click()
        except (AgentQLServerError, AttributeNotFoundError) as e:
            raise UnableToClosePopupError() from e
