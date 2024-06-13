from typing_extensions import TypeAlias
from _typeshed import StrPath
from pathlib import Path

UUIDStr: TypeAlias = str
UrlPath: TypeAlias = StrPath
ClassType: TypeAlias = object
RaliumIdStr: TypeAlias = UUIDStr

AbsolutePath: TypeAlias = Path
RelativePath: TypeAlias = Path

__version__: str