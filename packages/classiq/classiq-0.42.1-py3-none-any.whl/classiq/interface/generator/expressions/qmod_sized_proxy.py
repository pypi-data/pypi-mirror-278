from typing import TYPE_CHECKING, Any, Mapping

from classiq.exceptions import ClassiqNotImplementedError

if TYPE_CHECKING:
    from classiq.interface.model.handle_binding import HandleBinding


class QmodSizedProxy:
    def __init__(self, size: int) -> None:
        self._size = size

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        return str(self.handle)

    @property
    def type_name(self) -> str:
        raise NotImplementedError

    @property
    def handle(self) -> "HandleBinding":
        raise ClassiqNotImplementedError("cannot compute handle")

    @property
    def len(self) -> int:
        return self._size

    @property
    def fields(self) -> Mapping[str, Any]:
        return {}
