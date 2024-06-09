import sys
import pyfyre
from typing import Type
from browser import document
from types import TracebackType
from pyfyre.styles import Style
from pyfyre.states import StateDependency, State
from abc import ABC, abstractmethod
from browser import DOMNode, DOMEvent
from typing import Any, Dict, List, Optional, Callable, Union


class Node(ABC):
    """Represents an HTML DOM node.

    Attributes:
        dom (DOMNode): Brython ``DOMNode`` type.
            The corresponding HTML DOM node of this object.
    """

    def __init__(self) -> None:
        self.dom: DOMNode = self.create_dom()

    @abstractmethod
    def create_dom(self) -> DOMNode:
        raise NotImplementedError

    @abstractmethod
    def update_dom(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def html(self) -> str:
        """HTML representation of this object."""
        raise NotImplementedError


class Element(Node):
    """Represents an HTML DOM element.

    Args:
        tag_name: HTML tag name of this element.
        children: Builder for the children nodes of this element.
        styles: CSS styling of this element.
            This will be combined into a single ``Style`` object.
            The styles are evaluated in order from left to right.
        states: State dependencies of this object.
            If one of the state dependencies has changed its state,
            the ``update_dom`` method of this object will be called.
        attrs: HTML attributes of this element.

    Attributes:
        tag_name (str): HTML tag name of this element.
        children (List[Node]): Children nodes of this element.
            This is equal to the return of the ``children`` argument.
        style (~pyfyre.Style): CSS styling of this element.
        states (List[~pyfyre.StateDependency]): State dependencies of this object.
            If one of the state dependencies has changed its state,
            the ``update_dom`` method of this object will be called.
        attrs (Dict[str, str]): HTML attributes of this element.
    """

    def __init__(
        self,
        tag_name: str,
        children: Optional[Callable[[], List[Node]]] = None,
        *,
        styles: Optional[List[Style]] = None,
        states: Optional[List[StateDependency]] = None,
        attrs: Optional[Dict[str, str]] = None,
    ) -> None:
        self.tag_name = tag_name
        self.children: List[Node] = []
        self.style = Style.from_styles(styles) if styles else Style()
        self.states = states or []
        self.attrs = attrs or {}

        def children_builder() -> List[Node]:
            if children is None:
                return self.children

            try:
                return children()
            except Exception:
                return self.on_build_error(*sys.exc_info())

        self._children_builder = children_builder

        def update_style_attr() -> None:
            self.attrs = attrs or {}

            if "style" in self.attrs:
                self.attrs["style"] += f"; {self.style.css()}"
            else:
                self.attrs["style"] = self.style.css()

            if getattr(self, "dom", None) is not None:
                self.dom.setAttribute("style", self.attrs["style"])

        self.style.add_listener(update_style_attr)
        if self.style.props:
            update_style_attr()

        for state in self.states:
            state.add_listener(self.update_dom)

        super().__init__()

    def on_build_error(
        self,
        exc_type: Type[Exception],
        exc_value: Exception,
        exc_traceback: TracebackType,
    ) -> List[Node]:
        """:meta private:"""
        if pyfyre.PRODUCTION:
            from pyfyre.presets.errors import ErrorMessage

            return [ErrorMessage("An error occurred while loading this element")]

        from pyfyre.presets.errors import DebugError

        return [
            DebugError(
                exc_type=exc_type,
                exc_value=exc_value,
                exc_traceback=exc_traceback,
            )
        ]

    def build_children(self, *, propagate: bool = True) -> None:
        """:meta private:"""
        self.dom.clear()
        self.children = self._children_builder()

        for child in self.children:
            self.dom.attach(child.dom)

            if propagate and isinstance(child, Element):
                child.build_children()

    def create_dom(self) -> DOMNode:
        """Create a new HTML DOM element from this object.

        Returns:
            Brython ``DOMNode`` type.
        """
        el = document.createElement(self.tag_name)

        for attr_name, attr_value in self.attrs.items():
            el.setAttribute(attr_name, attr_value)

        return el

    def update_dom(self) -> None:
        """Update the corresponding HTML DOM element of this object.
        This rebuilds the children of this element recursively.
        """
        self.update_attrs()
        self.build_children(propagate=False)

        for child in self.children:
            child.update_dom()

    def update_attrs(self) -> None:
        """Update the attributes of the corresponding HTML DOM element of this object."""
        for attr_name, attr_value in self.attrs.items():
            self.dom.setAttribute(attr_name, attr_value)

    def is_void(self) -> bool:
        """Whether this element is a void or not based on its tag name.

        More about void elements:
            https://developer.mozilla.org/en-US/docs/Glossary/Void_element
        """
        return self.tag_name in (
            "area",
            "base",
            "br",
            "col",
            "embed",
            "hr",
            "img",
            "input",
            "keygen",
            "link",
            "meta",
            "param",
            "source",
            "track",
            "wbr",
        )

    def html(self) -> str:
        def attributes() -> str:
            attrs = [f'{name}="{value}"' for name, value in self.attrs.items()]
            return " " + " ".join(attrs) if attrs else ""

        result = f"<{self.tag_name}{attributes()}>"

        if self.is_void():
            return result

        for child in self.children:
            result += child.html()

        return result + f"</{self.tag_name}>"

    def add_event_listener(
        self, event_type: str, callback: Callable[[DOMEvent], None]
    ) -> None:
        """Calls the ``callback`` whenever the specified ``event_type``
        is delivered to this element.
        """
        self.dom.bind(event_type, callback)


class TextNode(Node):
    """Represents an HTML DOM text node.

    Args:
        *values: Value of the text.
            You can pass in a ``State`` object to automatically update the value of the text
            when the state dependency has changed its state.
    """

    def __init__(self, *values: Union[State[Any], Any]) -> None:
        self._value = self._process_values(*values)
        super().__init__()

    def _process_values(self, *values: Union[State[Any], Any]) -> str:
        def add_values() -> str:
            result = ""

            for value in values:
                if isinstance(value, State):
                    result += str(value.value)
                else:
                    result += str(value)

            return result

        def update_value() -> None:
            self._value = add_values()
            self.update_dom()

        for value in values:
            if isinstance(value, State):
                value.add_listener(update_value)

        return add_values()

    @property
    def value(self) -> str:
        """Value of the text."""
        self._value = self.dom.nodeValue
        return self._value

    def create_dom(self) -> DOMNode:
        """Create a new HTML DOM text node from this object.

        Returns:
            Brython ``DOMNode`` type.
        """
        return document.createTextNode(self._value)

    def update_dom(self) -> None:
        """:meta private:"""
        self.dom.nodeValue = self._value

    def html(self) -> str:
        return self._value


E = Element
Text = TextNode
