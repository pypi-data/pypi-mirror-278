from settings import ROUTES
from typing import Any, Dict, Callable, Optional
from browser import document, window, DOMEvent
from pyfyre.events import window_event_listener
from pyfyre.nodes import Node, Element, TextNode


class _NavigationStack:
    def __init__(self, initial_route: str) -> None:
        self._data = [initial_route]

    @property
    def top(self) -> str:
        return self._data[-1]

    def push(self, route: str) -> None:
        self._data.append(route)

    def pop(self) -> str:
        return self._data.pop()


class RouteManager:
    """A static class that enables navigation between various views in a PyFyre application."""

    _stack: _NavigationStack
    _routes_builder: Dict[str, Callable[..., Node]] = {}
    _routes: Dict[str, Optional[Node]] = {}
    _root_node = document.select_one("#root")

    @staticmethod
    def initialize(routes: Dict[str, Callable[..., Node]]) -> None:
        """:meta private:"""
        initial_route = RouteManager.parse_route(window.location.href)
        RouteManager._stack = _NavigationStack(initial_route)
        RouteManager._routes_builder = routes

        @window_event_listener("popstate")
        def onpopstate(event: DOMEvent) -> None:
            RouteManager.change_route(window.location.href)

    @staticmethod
    def parse_route(route_name: str) -> str:
        """Parse the ``route_name`` to turn it into a valid route name.

        Examples:
            | ``home`` -> ``/home``
            | ``contact/`` -> ``/contact``
            | ``about/this`` -> ``/about/this``
            | ``https://pyfyre.app/`` -> ``/``
            | ``https://pyfyre.app/about`` -> ``/about``
        """

        el = document.createElement("a")
        el.href = route_name
        route_name = str(el.pathname)

        if route_name == "/":
            return route_name

        return str(el.pathname).rstrip("/")

    @staticmethod
    def get_node(
        route_name: str,
        *,
        arg: Any = None,
        force_build: bool = True,
        parse_route: bool = True,
    ) -> Optional[Node]:
        """Call the corresponding route builder of the ``route_name``
        and return its ``Node``.

        Args:
            arg: The argument that will be passed in to the route builder.
            force_build: Whether to call the route builder even if it is already called before.
                By default, called route builders are cached.
            parse_route: Whether to call the
                ``RouteManager.parse_route`` method on the ``route_name``.

        Returns:
            The returned ``Node`` of the corresponding route builder of the ``route_name``.
            If the route doesn't exist, the default will be returned
            which has a 404 message.
        """

        if parse_route:
            route_name = RouteManager.parse_route(route_name)

        node = RouteManager._routes.get(route_name)

        if force_build or node is None:
            route_builder = RouteManager._routes_builder.get(route_name)

            if route_builder is not None:
                try:
                    node = route_builder(arg)
                except TypeError:
                    node = route_builder()
            else:
                node = None

            RouteManager._routes[route_name] = node

            if isinstance(node, Element):
                node.build_children()

        return node

    @staticmethod
    def render_route(
        route_name: str, *, arg: Any = None, force_build: bool = True
    ) -> None:
        """:meta private:"""
        node = RouteManager.get_node(
            route_name, arg=arg, force_build=force_build
        ) or TextNode("No route to render.")
        RouteManager._root_node.clear()
        RouteManager._root_node.attach(node.dom)

    @staticmethod
    def _update_page(
        route_data: Dict[str, Any], prev_route_data: Dict[str, Any]
    ) -> bool:
        if (route_data.get("head") or []) != (prev_route_data.get("head") or []):
            return False

        document.title = route_data.get("title")

        icon = document.select_one("link[rel~='icon']")
        if icon is not None:
            icon.href = route_data.get("icon")

        return True

    @staticmethod
    def _get_url(route_name: str) -> str:
        """Get the URL of the page the ``route_name`` goes to."""
        el = document.createElement("a")
        el.href = route_name
        return str(el.href + window.location.hash)

    @staticmethod
    def change_route(
        route_name: str, *, arg: Any = None, force_build: bool = True
    ) -> None:
        """Change the current route.

        This adds an entry to the browser's session history stack.

        If the ``route_name`` is not present in the ``ROUTES``
        in your ``settings.py`` file, `404 Not Found` will be returned.

        If the ``ROUTES[route_name]["head"]`` (head data)
        is not equal to the head data of the current route, the page will reload.
        This is because it is really not allowed to modify the head tag in HTML.

        Args:
            route_name: The name of the route that will be rendered.
            arg: The argument that will be passed in to the route builder.
            force_build: Whether to call the route builder even if it is already called before.
                By default, called route builders are cached.
        """
        route_name = RouteManager.parse_route(route_name)
        prev_route = RouteManager._stack.top
        route_data = ROUTES.get(route_name)

        window.history.pushState(None, None, RouteManager._get_url(route_name))
        RouteManager._stack.push(route_name)

        if route_data is None:
            window.location.reload()
        else:
            has_same_head = RouteManager._update_page(route_data, ROUTES[prev_route])
            if has_same_head:
                RouteManager.render_route(route_name, arg=arg, force_build=force_build)
            else:
                window.location.reload()
