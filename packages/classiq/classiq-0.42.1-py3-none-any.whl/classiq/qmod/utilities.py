import inspect
import itertools
import keyword
import sys
from types import FrameType
from typing import get_args, get_origin

from classiq.interface.ast_node import SourceReference

DEFAULT_DECIMAL_PRECISION = 4


def mangle_keyword(name: str) -> str:
    if keyword.iskeyword(name):
        name = f"{name}_"
    return name


def unmangle_keyword(name: str) -> str:
    assert name
    if name[-1] == "_" and keyword.iskeyword(name[:-1]):
        name = name[:-1]
    return name


def version_portable_get_args(py_type: type) -> tuple:
    if get_origin(py_type) is None:
        return tuple()
    if sys.version_info[0:2] < (3, 10):
        return get_args(py_type)  # The result of __class_getitem__
    else:
        return get_args(py_type)[0]


def get_source_ref(frame: FrameType) -> SourceReference:
    filename = inspect.getfile(frame)
    lineno = frame.f_lineno
    if sys.version_info[0:2] < (3, 11) or frame.f_lasti < 0:
        source_ref = SourceReference(
            file_name=filename,
            start_line=lineno - 1,
            start_column=-1,
            end_line=-1,
            end_column=-1,
        )
    else:
        positions_gen = frame.f_code.co_positions()
        positions = next(itertools.islice(positions_gen, frame.f_lasti // 2, None))
        source_ref = SourceReference(
            file_name=filename,
            start_line=(positions[0] or 0) - 1,
            start_column=(positions[2] or 0) - 1,
            end_line=(positions[1] or 0) - 1,
            end_column=(positions[3] or 0) - 1,
        )
    return source_ref
