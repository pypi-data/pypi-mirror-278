#
# MIT License
#
# Copyright (c) 2024 nbiotcloud
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""Utilities."""

import sys
from collections.abc import Iterable
from contextlib import contextmanager
from functools import lru_cache
from inspect import getfile
from pathlib import Path
from typing import Any


@contextmanager
def extend_sys_path(paths: Iterable[Path]):
    """Context with extended sys.path.

    Args:
        paths: Paths
    """
    pathstrs = [str(path) for path in paths]
    if pathstrs:
        orig = sys.path
        sys.path = [*sys.path, *pathstrs]
        yield
        sys.path = orig
    else:
        yield


def get_copyright(obj: Any) -> str:
    """Determine from Source Code of ``obj``."""
    if isinstance(obj, Path):
        path = obj
    elif isinstance(obj, object):
        path = Path(getfile(obj.__class__))
    else:
        path = Path(getfile(obj))
    return _get_copyright(path)


@lru_cache
def _get_copyright(path: Path) -> str:
    lines = []
    with path.open(encoding="utf-8") as file:
        for line in file:
            if line.startswith("#"):
                lines.append(line[1:])
            else:
                break
    return "".join(lines)
