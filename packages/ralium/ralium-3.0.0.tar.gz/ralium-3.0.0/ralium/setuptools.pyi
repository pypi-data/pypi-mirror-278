from collections.abc import Iterable
from ralium.util import AbsolutePath
from _typeshed import StrOrBytesPath
from pathlib import Path
from typing import overload

@overload
def bundle(
    pyfile: StrOrBytesPath,
    project: StrOrBytesPath,
    filename: str | None = ...,
    distpath: StrOrBytesPath | None = ...
) -> AbsolutePath: ...
@overload
def bundle(
    pyfile: Path,
    project: Path,
    filename: str | None = ...,
    distpath: Path | None = ...
) -> AbsolutePath: ...

@overload
def setup(
    pyfile: StrOrBytesPath | Path,
    name: str | None = ...,
    icon: StrOrBytesPath | Path | None = ...,
    bundle: bool = False,
    project: StrOrBytesPath | Path | None = ...,
    onefile: bool = True,
    noconsole: bool = True,
    bundle_dist: StrOrBytesPath | Path | None = ...,
    optimize: int | None = ...,
    pyi_args: Iterable[str] | None = ...,
    use_subprocess: bool = False,
) -> None: ...
@overload
def setup(
    pyfile: Path,
    name: str | None = ...,
    icon: Path | None = ...,
    bundle: bool = False,
    project: Path | None = ...,
    onefile: bool = True,
    noconsole: bool = True,
    bundle_dist: Path | None = ...,
    optimize: int | None = ...,
    pyi_args: Iterable[str] | None = ...,
    use_subprocess: bool = False,
) -> None: ...