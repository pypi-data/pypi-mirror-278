from abc import abstractmethod
from typing import Any, Dict, List, Literal, Union

import pydantic
from pydantic import Extra, Field
from sympy import IndexedBase, Symbol
from typing_extensions import Annotated

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.generator.expressions.enums.classical_enum import ClassicalEnum
from classiq.interface.generator.expressions.enums.ladder_operator import (
    LadderOperator as LadderOperatorEnum,
)
from classiq.interface.generator.expressions.enums.pauli import Pauli as PauliEnum
from classiq.interface.generator.expressions.expression_types import RuntimeExpression
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator

CLASSICAL_ATTRIBUTES = {"len", "size", "is_signed", "fraction_digits"}

NamedSymbol = Union[IndexedBase, Symbol]


class ClassicalType(HashableASTNode):
    def as_symbolic(self, name: str) -> Union[NamedSymbol, List[NamedSymbol]]:
        return Symbol(name)

    @property
    @abstractmethod
    def default_value(self) -> Any:
        raise NotImplementedError(
            f"{self.__class__.__name__} type has no default value"
        )

    @property
    def qmod_type(self) -> type:
        raise NotImplementedError(
            f"{self.__class__.__name__!r} has no QMOD SDK equivalent"
        )

    class Config:
        extra = Extra.forbid

    def __str__(self) -> str:
        return str(type(self).__name__)


class EnumType(ClassicalType):
    pass


class Integer(ClassicalType):
    kind: Literal["int"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, integer=True)

    @property
    def default_value(self) -> int:
        return 0

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "int")

    @property
    def qmod_type(self) -> type:
        from classiq.qmod.qmod_parameter import CInt

        return CInt


class Real(ClassicalType):
    kind: Literal["real"]

    def as_symbolic(self, name: str) -> Symbol:
        return Symbol(name, real=True)

    @property
    def default_value(self) -> float:
        return 0.0

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "real")

    @property
    def qmod_type(self) -> type:
        from classiq.qmod.qmod_parameter import CReal

        return CReal


class Bool(ClassicalType):
    kind: Literal["bool"]

    @property
    def default_value(self) -> bool:
        return False

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "bool")

    @property
    def qmod_type(self) -> type:
        from classiq.qmod.qmod_parameter import CBool

        return CBool


class ClassicalList(ClassicalType):
    kind: Literal["list"]
    element_type: "ConcreteClassicalType"

    def as_symbolic(self, name: str) -> Symbol:
        return IndexedBase(name)

    @property
    def default_value(self) -> List:
        return []

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "list")

    @property
    def qmod_type(self) -> type:
        from classiq.qmod.qmod_parameter import CArray

        return CArray[self.element_type.qmod_type]  # type:ignore[name-defined]


class Pauli(EnumType):
    kind: Literal["pauli"]

    @property
    def default_value(self) -> PauliEnum:
        return PauliEnum.I

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "pauli")

    @property
    def qmod_type(self) -> type:
        return PauliEnum


class StructMetaType(ClassicalType):
    kind: Literal["type_proxy"]

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "type_proxy")


class CStructBase:  # marker for Qmod structs in the Python SDK
    pass


class Struct(ClassicalType):
    kind: Literal["struct_instance"]
    name: str = pydantic.Field(description="The struct type of the instance")

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "struct_instance")

    @property
    def qmod_type(self) -> type:
        return type(self.name, (CStructBase,), dict())


class ClassicalArray(ClassicalType):
    kind: Literal["array"]
    element_type: "ConcreteClassicalType"
    size: pydantic.PositiveInt

    def as_symbolic(self, name: str) -> list:
        return [self.element_type.as_symbolic(f"{name}_{i}") for i in range(self.size)]

    @property
    def default_value(self) -> Any:
        return super().default_value

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "array")

    @property
    def qmod_type(self) -> type:
        from classiq.qmod.qmod_parameter import CArray

        return CArray[
            self.element_type.qmod_type, self.size  # type:ignore[name-defined]
        ]


class OpaqueHandle(ClassicalType):
    @property
    def default_value(self) -> int:
        return 0


class VQEResult(OpaqueHandle):
    kind: Literal["vqe_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "vqe_result")


class Histogram(OpaqueHandle):
    kind: Literal["histogram"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "histogram")


class Estimation(OpaqueHandle):
    kind: Literal["estimation_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "estimation_result")


class IQAERes(OpaqueHandle):
    kind: Literal["iqae_result"]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "iqae_result")


class LadderOperator(EnumType):
    kind: Literal["ladder_operator"]

    @property
    def default_value(self) -> LadderOperatorEnum:
        return LadderOperatorEnum.PLUS

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "ladder_operator")

    @property
    def qmod_type(self) -> type:
        return LadderOperatorEnum


ConcreteClassicalType = Annotated[
    Union[
        Integer,
        Real,
        Bool,
        ClassicalList,
        Pauli,
        StructMetaType,
        Struct,
        ClassicalArray,
        VQEResult,
        Histogram,
        Estimation,
        LadderOperator,
        IQAERes,
    ],
    Field(discriminator="kind"),
]
ClassicalList.update_forward_refs()
ClassicalArray.update_forward_refs()

PythonClassicalTypes = (int, float, bool, list, CStructBase, ClassicalEnum)


def as_symbolic(symbols: Dict[str, ClassicalType]) -> Dict[str, RuntimeExpression]:
    return {
        param_name: param_type.as_symbolic(param_name)
        for param_name, param_type in symbols.items()
    }


class QmodPyObject:
    pass
