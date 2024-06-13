from _typeshed import StrOrBytesPath
from typing import Tuple, Dict, Any

class WindowConfig:
    def __init__(self,
        title: str = ...,
        icon: StrOrBytesPath | None = ...,
        size: Tuple[int, int] = (900, 600), 
        min_size: Tuple[int, int] = (300, 300), 
        resizable: bool = True,
        use_builtins: bool = True,
        **kwargs: Dict[str, Any]
    ) -> None: ...
    
    def as_webview_kwargs(self) -> Dict[str, Any]: ...