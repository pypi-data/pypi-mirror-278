from pyfyre.styles import Style
from pyfyre.states import StateDependency
from pyfyre.nodes.base import Node, Element
from browser import DOMEvent, window, document
from typing import Any, Optional, Dict, List, Callable


class Link(Element):
    """Represents an HTML ``<a>``.

    Args:
        href: Hyperlink of the page the link goes to.

    Attributes:
        href (str): Hyperlink of the page the link goes to.
    """

    def __init__(
        self,
        href: str,
        children: Optional[Callable[[], List[Node]]] = None,
        *,
        styles: Optional[List[Style]] = None,
        states: Optional[List[StateDependency]] = None,
        attrs: Optional[Dict[str, str]] = None
    ) -> None:
        self.href = href
        attrs = attrs or {}
        attrs["href"] = href
        super().__init__("a", children, styles=styles, states=states, attrs=attrs)

    @property
    def url(self) -> str:
        """URL of the page the link goes to."""
        el = document.createElement("a")
        el.href = self.href
        return el.href

    def is_internal(self) -> bool:
        """Whether the href is linked within the same domain."""
        el = document.createElement("a")
        el.href = self.href
        return bool(el.host == window.location.host)


class RouterLink(Link):
    """Navigates to a different route inside the website as a single-page application.

    Args:
        arg: The argument that will be passed in to the route builder.
        force_build: Whether to call the route builder even if it is already called before.
            By default, called route builders are cached.
    """

    def __init__(
        self,
        href: str,
        children: Optional[Callable[[], List[Node]]] = None,
        *,
        arg: Any = None,
        force_build: bool = True,
        styles: Optional[List[Style]] = None,
        attrs: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(href, children, styles=styles, attrs=attrs)

        def change_route(event: DOMEvent) -> None:
            # Import here due to cicular import problem
            from pyfyre.router import RouteManager

            event.preventDefault()
            RouteManager.change_route(href, arg=arg, force_build=force_build)

        self.add_event_listener("click", change_route)
