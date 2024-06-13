from ralium.element import HTMLElement
from ralium.window import Window
from ralium.util import UrlPath

from collections.abc import Callable
from typing import List, Any
from types import FunctionType

__registry__: List[FunctionType]

def builtin(function: FunctionType) -> Callable[..., Any]: ...

@builtin
def refresh(window: Window) -> None: ...
@builtin
def redirect(window: Window, url: UrlPath) -> None: ...
@builtin
def shutdown(window: Window) -> None: ...
@builtin
def getUrl(window: Window, element: HTMLElement | None = ...) -> UrlPath: ...
@builtin
def getServerPort(window: Window, element: HTMLElement | None = ...) -> int: ...