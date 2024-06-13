from typing import Protocol, Any

from agentql.experimental import InteractiveItemTypeT, PageTypeT


class Page(Protocol[InteractiveItemTypeT, PageTypeT]):
    """
    The Page protocol represents a sync implementation of browser page (tab) which can be queried and interacted with.
    """

    page: PageTypeT
    """A driver-specific page interface, assigned during __init__."""

    _check_popup: bool
    _event_listeners: dict
    _current_tf_id: Any
    _page_monitor: Any
    _last_accessibility_tree: Any

    @property
    def url(self) -> str:
        raise NotImplementedError()

    @property
    def _accessibility_tree(self) -> dict:
        raise NotImplementedError()

    def open(self, url: str):
        """
        Open a new URL inside a page.

        Parameters:
        -----------
        url (str): The URL to open.
        """
        raise NotImplementedError()

    def close(self):
        """
        Closes the page.
        """
        raise NotImplementedError()

    def _prepare_accessibility_tree(self, include_aria_hidden: bool) -> dict:
        """
        Prepare the accessibility tree by modifing the dom. It will return the accessibility tree after waiting for page to load and dom modification.

        Parameters:
        -----------
        include_aria_hidden: Whether to include elements with aria-hidden attribute in the AT.

        Returns:
        --------
        dict: The accessibility tree of the page in Python Dict format.
        """
        raise NotImplementedError()

    def wait_for_page_ready_state(self, wait_for_network_idle: bool = True):
        """
        Wait for the page to reach the "Page Ready" state (i.e. page has entered a relatively stable state and most main content is loaded).

        Parameters:
        -----------
        wait_for_network_idle (bool) (optional): This acts as a switch to determine whether to use default chekcing mechanism. If set to `False`, this method will only check for whether page has emitted `load` [event](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event) and provide a less costly checking mechanism for fast-loading pages.
        """
        raise NotImplementedError()

    def _locate_interactive_element(self, response_data: dict) -> InteractiveItemTypeT:
        """
        Locates an interactive element in the web page.

        Parameters:
        -----------
        response_data (dict): The data of the interactive element from the AgentQL response.

        Returns:
        --------
        InteractiveItemTypeT: The interactive element.
        """
        raise NotImplementedError()

    def _get_text_content(self, web_element: InteractiveItemTypeT) -> str | None:
        """
        Gets the text content of the web element.

        Parameters:
        -----------
        web_element (InteractiveItemTypeT): The web element to get text from.

        Returns:
        --------
        str: The text content of the web element.
        """
        raise NotImplementedError()

    def _close_popup(self, popup_tree: dict, page_url: str, timeout: int = 500):
        """
        Close the popup on the page.

        Parameters:
        -----------
        popup_tree (dict): The accessibility tree that has the popup node as the parent.
        page_url (str): The URL of the active page.
        timeout (int) (optional): The timeout value for the connection with AgentQL server service.
        """
        raise NotImplementedError()
