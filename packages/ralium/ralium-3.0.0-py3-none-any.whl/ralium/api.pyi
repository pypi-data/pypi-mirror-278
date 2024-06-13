from ralium.web.webhook import WebHook
from ralium.config import WindowConfig
from ralium.window import Window
from ralium.util import AbsolutePath

from collections.abc import Callable
from _typeshed import StrPath, BytesPath
from types import FunctionType
from pathlib import Path

from typing import (
    overload,
    Tuple,
    Dict,
    List,
    Any
)

def check_project_path(project: AbsolutePath) -> None: ...
def check_routes_path(routes: AbsolutePath) -> None: ...
def collect_project_shared_styles(project: AbsolutePath) -> List[AbsolutePath]: ...
def get_server_registry_contents(source: AbsolutePath) -> List[FunctionType | WebHook.Namespace]: ...
def get_server_registry_objects(source: AbsolutePath) -> Tuple[List[FunctionType], List[WebHook.Namespace]]: ...
def collect_webhooks(project: AbsolutePath, routes: AbsolutePath) -> List[WebHook]: ...

class Module:
    _module_api_class: bool
    
    def __init__(self, 
        *functions: Tuple[FunctionType], 
        **named_functions: Dict[str, FunctionType]
    ) -> None: ...

@overload
def create_window(project: Path, config: WindowConfig | None = ...) -> Window: ...
@overload
def create_window(project: StrPath, config: WindowConfig | None = ...) -> Window: ...
@overload
def create_window(project: BytesPath, config: WindowConfig | None = ...) -> Window: ...

def register() -> Callable[..., Any]: ...
def namespace(
    alias: str, 
    *functions: Tuple[FunctionType], 
    **named_functions: Dict[str, FunctionType]
) -> None: ...

def wrap(function: FunctionType) -> Callable[..., Any]: ...