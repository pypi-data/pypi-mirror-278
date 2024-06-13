from ralium.web.webhook import WebHook
from typing import (
    LiteralString, 
    FunctionType, 
    Tuple, 
    Dict, 
    List, 
    Any
)

class PyHTML:
    __slots__: Tuple[LiteralString]

    def __init__(self, webhook: WebHook) -> None: ...
    def compile(self) -> str: ...
    def process(self, blocks: List[str]) -> List[str]: ...
    @staticmethod
    def locals(webhook: WebHook) -> Dict[str, Any]: ...
    @staticmethod
    def get_outcome(code: str, locals: Dict[str, FunctionType]) -> List[str]: ...
    @staticmethod
    def get_enclosed(text: str, start: str, end: str) -> List[str]: ...
    @staticmethod
    def removeaffix(text: str, prefix: str, suffix: str) -> str: ...