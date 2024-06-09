![image](https://user-images.githubusercontent.com/64759159/151080177-2b2ab45a-86e5-4746-b92f-6c4edd1aaa8f.png)

# PyFyre - The Python Web Frontend Framework
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![GitHub Version](https://img.shields.io/github/release/pyfyre/pyfyre.svg?style=for-the-badge)](https://github.com/pyfyre/pyfyre/releases)
[![Github Star](https://img.shields.io/github/stars/pyfyre/pyfyre.svg?style=for-the-badge)](https://github.com/pyfyre/pyfyre/stargazers) 
[![License](https://img.shields.io/github/license/pyfyre/pyfyre.svg?style=for-the-badge)](https://github.com/pyfyre/pyfyre/blob/main/LICENSE)

A fast, declarative, and incrementally adoptable Python web frontend framework for building reactive web user interfaces.

## Features
- **Component-based framework**. Developers who have experience in using other frontend frameworks should feel quite at home when using PyFyre.
- **Truly reactive**. PyFyre's virtual DOM allows for simple and efficient state management.
- **Quick navigation**. Navigation between pages is quick with PyFyre's single-page application design.
- **Pythonic code with static typing**. Developing with PyFyre is much easier with its type hinting and Pythonic style of coding.
- **Asynchronous programming**. Run non-blocking functions out of the box.
- **CPython interoperability**. Developers can limitedly use CPython packages on the client-side web.
- **JavaScript interoperability**. Allowing developers to leverage NPM packages and integrate with existing JavaScript applications.
- **Pure Python**. Build web apps without ever touching other languages like HTML and JavaScript.
- **And more!**

## Example
See the [examples](examples) directory for more.
If you want to quickly test how PyFyre feels or looks like, try our [playground](https://pyfyre.netlify.app/playground/)!
But here is a super simple example. See how easy it is to create a simple Counter app with PyFyre:
```py
from browser import DOMEvent
from pyfyre import render, State
from pyfyre.nodes import Node, Widget, Text, Button


class App(Widget):
    def __init__(self) -> None:
        self.count = State[int](0)
        super().__init__()

    def build(self) -> list[Node]:
        def increment(event: DOMEvent) -> None:
            self.count.set_value(self.count.value + 1)

        def decrement(event: DOMEvent) -> None:
            self.count.set_value(self.count.value - 1)

        return [
            Button(onclick=decrement, children=lambda: [Text("-")]),
            Text(self.count),
            Button(onclick=increment, children=lambda: [Text("+")]),
        ]


render({"/": lambda: App()})
```

## Documentation
Learn PyFyre by reading the [documentation](https://pyfyre-docs.netlify.app/).
It is also advisable to learn [Brython](https://www.brython.info/) alongside PyFyre as it is built on top of Brython.

## Links
- [PyPI](https://pypi.org/project/pyfyre/)
- [Repository](https://github.com/pyfyre/pyfyre)
- [Documentation](https://pyfyre-docs.netlify.app/)
- [Facebook Page](https://www.facebook.com/pyfyreframework/)
- [Discord Server](https://discord.gg/YzEDuqhgZJ)
