from typing import Any, Mapping, Optional, Tuple, Union

from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)

from classiq.exceptions import ClassiqValueError

ILLEGAL_SLICING_STEP_MSG = "Slicing with a step of a quantum variable is not supported"
SLICE_OUT_OF_BOUNDS_MSG = "Slice end index out of bounds"
QARRAY_ELEMENT_NOT_SUBSCRIPTABLE = "Subscripting an element in QArray is illegal"


class QmodQArrayProxy(QmodSizedProxy):
    def __init__(
        self,
        name: str,
        size: int,
        slice_: Optional[Tuple[int, int]] = None,
        index_: Optional[int] = None,
    ) -> None:
        super().__init__(size)
        self._name = name
        self._slice = slice_
        self._index = index_

    def __getitem__(self, key: Union[slice, int]) -> "QmodQArrayProxy":
        if self._index is not None:
            raise ClassiqValueError(QARRAY_ELEMENT_NOT_SUBSCRIPTABLE)

        new_index: Optional[int] = None

        if isinstance(key, slice):
            if key.step is not None:
                raise ClassiqValueError(ILLEGAL_SLICING_STEP_MSG)
            new_slice = self._get_new_slice(key.start, key.stop)
        else:
            new_slice = self._get_new_slice(key, key + 1)
            new_index = new_slice[0]

        if (self._slice is not None and new_slice[1] > self._slice[1]) or new_slice[
            1
        ] > self._size:
            raise ClassiqValueError(SLICE_OUT_OF_BOUNDS_MSG)

        return QmodQArrayProxy(
            self._name, self._size, slice_=new_slice, index_=new_index
        )

    def _get_new_slice(self, start: int, end: int) -> Tuple[int, int]:
        if self._slice is not None:
            return self._slice[0] + start, self._slice[0] + end
        return start, end

    @property
    def type_name(self) -> str:
        return "Quantum array"

    @property
    def index(self) -> Optional[int]:
        return self._index

    @property
    def slice(self) -> Optional[Tuple[int, int]]:
        return self._slice

    @property
    def handle(self) -> HandleBinding:
        if self._index is not None:
            return SubscriptHandleBinding(
                name=self._name,
                index=Expression(expr=str(self._index)),
            )

        if self._slice is not None:
            return SlicedHandleBinding(
                name=self._name,
                start=Expression(expr=str(self._slice[0])),
                end=Expression(expr=str(self._slice[1])),
            )

        return HandleBinding(name=self._name)

    @property
    def fields(self) -> Mapping[str, Any]:
        return {
            "len": self.len,
        }

    def __len__(self) -> int:
        if (slice_ := self.slice) is not None:
            return slice_[1] - slice_[0]
        elif self.index is not None:
            return 1
        return self._size

    def __str__(self) -> str:
        return str(self.handle)
