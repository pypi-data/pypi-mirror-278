# pylint: disable=all

# It is a mixin class, so pylint complains about missing methods and variables, etc. I will fix that later.

from typing import Generic, Literal, List, Callable

from agentql.experimental.sync_api._response_proxy import AQLResponseProxy
from agentql.sync_api._agentql_service import query_agentql_server
from agentql.experimental import InteractiveItemTypeT, PageTypeT
from agentql.sync_api._popup import Popup
from agentql import QueryParser

import copy


class Query(Generic[InteractiveItemTypeT, PageTypeT]):  # type: ignore #TODO figure out how to handle warning smoothly.
    """
    An async mixin class used to reuse .query() implementation accross different Page implementations.
    """

    def query(
        self,
        query: str,
        timeout: int = 500,
        wait_for_network_idle: bool = True,
        include_aria_hidden: bool = False,
    ) -> AQLResponseProxy[InteractiveItemTypeT, PageTypeT]:
        """Query the web page tree for elements that match the AgentQL query.

        Parameters:
        ----------
        query (str): The AgentQL query in String format.
        timeout (int) (optional): Optional timeout value for the connection with backend api service.
        wait_for_network_idle (bool) (optional): Whether to wait for the network to be idle before querying the page.
        include_aria_hidden (bool) (optional): Whether to include elements with aria-hidden attribute in the accessibility tree.

        Returns:
        -------
        AQLResponseProxy: AgentQL Response (Elements that match the query) of AQLResponseProxy type.
        """
        parser = QueryParser(query)
        query_tree = parser.parse()

        self.wait_for_page_ready_state(wait_for_network_idle=wait_for_network_idle)

        accessibility_tree = self._prepare_accessibility_tree(
            include_aria_hidden=include_aria_hidden
        )

        # Check if there is a popup in the page before sending the agentql query
        popup_list = []
        if self._check_popup:
            popup_list = self._detect_popup(accessibility_tree, [])
            if popup_list:
                self._handle_popup(popup_list)
                accessibility_tree = self._prepare_accessibility_tree(
                    include_aria_hidden=include_aria_hidden,
                )

        self._last_accessibility_tree = accessibility_tree

        response = query_agentql_server(query, accessibility_tree, timeout, self.url)

        # Check if there is a popup in the page after receiving the agentql response
        if self._check_popup:
            # Fetch the most up-to-date accessibility tree
            accessibility_tree = self._accessibility_tree

            popup_list = self._detect_popup(accessibility_tree, popup_list)
            if popup_list:
                self._handle_popup(popup_list)
                accessibility_tree = self._prepare_accessibility_tree(
                    include_aria_hidden=include_aria_hidden,
                )

        self._last_accessibility_tree = accessibility_tree

        return AQLResponseProxy[InteractiveItemTypeT, PageTypeT](response, self, query_tree)

    def on(self, event: Literal["popup"], callback: Callable[[dict], None]):
        """Emitted when there is a popup (such as promotion window) on the page. The callback function will be invoked with the popup object as the argument. Passing None as the callback function will disable popup detections.

        Event Data:
        -----------
        popups (list): The list of popups captured on the page by AgentQL Popup Detection algorithm.
        """
        self._event_listeners[event] = callback
        if callback:
            self._check_popup = True
        else:
            self._check_popup = False

    def _detect_popup(self, tree: dict, known_popups: List[Popup]) -> List[Popup]:
        """Detect if there is a popup in the page. If so, create a Popup object and add it to the popup dict.

        Parameters:
        ----------
        tree (dict): The accessibility tree.
        known_popups (list): The list of known popups.

        Returns:
        --------
        popups (list): The list of popups.
        """
        tree_role = tree.get("role", "")
        tree_name = tree.get("name", "")
        popup_list = []
        if tree_role == "dialog":
            popup = Popup(
                self.url,
                copy.deepcopy(tree),
                tree_name,
                self._close_popup,  # type: ignore
            )

            # Avoid adding existing popup to the dict and double handle the popup
            if known_popups:
                for popup_object in known_popups:
                    if popup_object.name != popup.name:
                        popup_list.append(popup)
            else:
                popup_list.append(popup)

            return popup_list

        if "children" in tree:
            for child in tree.get("children", []):
                popup_list = popup_list + self._detect_popup(child, known_popups)

        return popup_list

    def _handle_popup(self, popups: List[Popup]):
        """Handle the popup. If there is a popup in the list, and there is an event listener, emit the popup event by invoking the callback function.

        Parameters:
        ----------
        popups (list): The list of popups to handle."""
        if popups and "popup" in self._event_listeners and self._event_listeners["popup"]:
            self._event_listeners["popup"](popups)
