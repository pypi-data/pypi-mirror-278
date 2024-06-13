from collections.abc import Callable, Iterable, Iterator
from ralium.util import UrlPath
from _typeshed import BytesPath, StrPath
from types import FunctionType
from pathlib import Path

from ..window import Window

from typing import (
    Concatenate, 
    overload,
    AnyStr, 
    _KT_co, 
    _VT_co,
    Tuple,
    Dict, 
    List, 
    Any
)

def create_namespace(
    alias: str, 
    *functions: Tuple[FunctionType], 
    **named_functions: Dict[str, FunctionType]
) -> WebHook.Namespace: ...

class WebHook:
    class Function:
        def __new__(cls, 
            function: Callable[Concatenate[Window, ...], Any], 
            window: Window
        ) -> Callable[..., Any]: ...

    class Namespace:
        def __init__(self, 
            alias: str, 
            *functions: Tuple[FunctionType], 
            **named_functions: Dict[str, FunctionType]
        ) -> None: ...

        def add(self, name: str, function: FunctionType) -> None: ...

        def add_functions(self, *functions: Tuple[FunctionType]) -> None: ...
        def add_named_functions(self, **functions: Dict[str, FunctionType]) -> None: ...

    class Collection(dict):
        def __init__(self, *webhooks: Tuple[WebHook]) -> None: ...
        def __iter__(self) -> Iterator[tuple[_KT_co, _VT_co]]: ...
        def __repr__(self) -> AnyStr: ...
        def get(self, url: UrlPath) -> WebHook: ...

    @overload
    def __init__(self, 
        url: UrlPath, 
        html: Path, 
        styles: List[Path] | None = ..., 
        functions: List[FunctionType] | None = ..., 
        namespaces: List[WebHook.Namespace] | None = ..., 
        encoding: str = "UTF-8"
    ) -> None: ...
    @overload
    def __init__(self, 
        url: UrlPath, 
        html: StrPath | str, 
        styles: List[StrPath] | None = ..., 
        functions: List[FunctionType] | None = ..., 
        namespaces: List[WebHook.Namespace] | None = ..., 
        encoding: str = "UTF-8"
    ) -> None: ...
    @overload
    def __init__(self, 
        url: UrlPath, 
        html: BytesPath | bytes, 
        styles: List[BytesPath] | None = ..., 
        functions: List[FunctionType] | None = ..., 
        namespaces: List[WebHook.Namespace] | None = ..., 
        encoding: str = "UTF-8"
    ) -> None: ...

    def __repr__(self) -> AnyStr: ...

    @property
    def html(self) -> AnyStr: ...
    @property
    def styles(self) -> List[AnyStr]: ...
    
    @html.setter
    def html(self, new_html: Path | StrPath | BytesPath) -> None: ...
    @styles.setter
    def styles(self, new_styles: Iterable[Path | StrPath | BytesPath]) -> None: ...
    
    @staticmethod
    def requires_window(function: FunctionType) -> Callable[Concatenate[WebHook, ...], Any]: ...
    
    @requires_window
    def wrap_function_objects(self) -> None: ...
    @requires_window
    def wrap_namespace_objects(self) -> None: ...
    
    @overload
    @staticmethod
    def _loads(path: Path, encoding: str = "UTF-8", file_type: str | None = ...) -> AnyStr: ...
    @overload
    @staticmethod
    def _loads(path: StrPath, encoding: str = "UTF-8", file_type: str | None = ...) -> AnyStr: ...
    @overload
    @staticmethod
    def _loads(path: BytesPath, encoding: str = "UTF-8", file_type: str | None = ...) -> AnyStr: ...
    
    @overload
    @staticmethod
    def load_html(path: Path, encoding: str = "UTF-8") -> AnyStr: ...
    @overload
    @staticmethod
    def load_html(path: StrPath, encoding: str = "UTF-8") -> AnyStr: ...  
    @overload
    @staticmethod
    def load_html(path: BytesPath, encoding: str = "UTF-8") -> AnyStr: ...  
   
    @overload
    @staticmethod
    def load_style(path: Path, encoding: str = "UTF-8") -> AnyStr: ...
    @overload
    @staticmethod
    def load_style(path: StrPath, encoding: str = "UTF-8") -> AnyStr: ...
    @overload
    @staticmethod
    def load_style(path: BytesPath, encoding: str = "UTF-8") -> AnyStr: ...