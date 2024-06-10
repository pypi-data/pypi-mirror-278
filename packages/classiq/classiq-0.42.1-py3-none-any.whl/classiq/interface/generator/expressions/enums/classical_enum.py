import enum
from typing import Any, Mapping

from classiq.interface.helpers.classproperty import classproperty


class ClassicalEnum(int, enum.Enum):
    def __str__(self) -> str:
        return f"{type(self).__name__}.{self.name}"

    def __repr__(self) -> str:
        return str(self)

    @classproperty
    def type_name(cls) -> str:  # noqa: N805
        return "Enum"

    @classproperty
    def fields(cls) -> Mapping[str, Any]:  # noqa: N805
        return {i.name: i for i in cls}  # type:ignore[attr-defined]
