from typing import Any, Dict, Literal, Optional, Union

import pydantic
from pydantic import Extra, Field
from typing_extensions import Annotated

from classiq.interface.ast_node import HashableASTNode
from classiq.interface.generator.arith.register_user_input import (
    RegisterArithmeticInfo,
    RegisterUserInput,
)
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.expressions.qmod_qarray_proxy import QmodQArrayProxy
from classiq.interface.generator.expressions.qmod_qscalar_proxy import (
    QmodQNumProxy,
    QmodQScalarProxy,
)
from classiq.interface.generator.expressions.qmod_sized_proxy import QmodSizedProxy
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator

from classiq.exceptions import ClassiqValueError


class QuantumType(HashableASTNode):
    class Config:
        extra = Extra.forbid

    _size_in_bits: Optional[int] = pydantic.PrivateAttr(default=None)

    def _update_size_in_bits_from_declaration(self) -> None:
        pass

    @property
    def size_in_bits(self) -> int:
        self._update_size_in_bits_from_declaration()
        if self._size_in_bits is None:
            raise ClassiqValueError("Trying to retrieve unknown size of quantum type")
        return self._size_in_bits

    @property
    def has_size_in_bits(self) -> bool:
        self._update_size_in_bits_from_declaration()
        return self._size_in_bits is not None

    def set_size_in_bits(self, val: int) -> None:
        self._size_in_bits = val

    def get_proxy(self, name: str) -> QmodSizedProxy:
        return QmodSizedProxy(size=self.size_in_bits)


class QuantumScalar(QuantumType):
    def get_proxy(self, name: str) -> QmodQScalarProxy:
        return QmodQScalarProxy(name, size=self.size_in_bits)


class QuantumBit(QuantumScalar):
    kind: Literal["qbit"]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._size_in_bits = 1

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qbit")


class QuantumBitvector(QuantumType):
    kind: Literal["qvec"]
    length: Optional[Expression]

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qvec")

    def _update_size_in_bits_from_declaration(self) -> None:
        if self.length is not None and self.length.is_evaluated():
            self._size_in_bits = self.length.to_int_value()

    def get_proxy(self, name: str) -> QmodQArrayProxy:
        return QmodQArrayProxy(name, self.size_in_bits)


class QuantumNumeric(QuantumScalar):
    kind: Literal["qnum"]

    size: Optional[Expression] = pydantic.Field()
    is_signed: Optional[Expression] = pydantic.Field()
    fraction_digits: Optional[Expression] = pydantic.Field()

    @pydantic.root_validator(pre=True)
    def _set_kind(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return values_with_discriminator(values, "kind", "qnum")

    @pydantic.root_validator
    def _validate_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        has_sign = values["is_signed"] is not None
        has_fraction_digits = values["fraction_digits"] is not None
        if has_sign and not has_fraction_digits or not has_sign and has_fraction_digits:
            raise ClassiqValueError(
                "Assign neither or both of is_signed and fraction_digits"
            )
        return values

    @property
    def has_sign(self) -> bool:
        return self.is_signed is not None

    @property
    def sign_value(self) -> bool:
        return False if self.is_signed is None else self.is_signed.to_bool_value()

    @property
    def has_fraction_digits(self) -> bool:
        return self.fraction_digits is not None

    @property
    def fraction_digits_value(self) -> int:
        return (
            0 if self.fraction_digits is None else self.fraction_digits.to_int_value()
        )

    def _update_size_in_bits_from_declaration(self) -> None:
        if self.size is not None and self.size.is_evaluated():
            self._size_in_bits = self.size.to_int_value()

    def get_proxy(self, name: str) -> QmodQNumProxy:
        return QmodQNumProxy(
            name,
            size=self.size_in_bits,
            fraction_digits=self.fraction_digits_value,
            is_signed=self.sign_value,
        )


ConcreteQuantumType = Annotated[
    Union[QuantumBit, QuantumBitvector, QuantumNumeric],
    Field(discriminator="kind", default_factory=QuantumBitvector),
]


def register_info_to_quantum_type(reg_info: RegisterArithmeticInfo) -> QuantumNumeric:
    result = QuantumNumeric()
    result.set_size_in_bits(reg_info.size)
    result.is_signed = Expression(expr=str(reg_info.is_signed))
    result.fraction_digits = Expression(expr=str(reg_info.fraction_places))
    return result


UNRESOLVED_SIZE = 1000


def quantum_var_to_register(name: str, qtype: QuantumType) -> RegisterUserInput:
    if isinstance(qtype, QuantumNumeric):
        signed = qtype.sign_value
        fraction_places = qtype.fraction_digits_value
    else:
        signed = False
        fraction_places = 0
    return RegisterUserInput(
        name=name,
        size=qtype.size_in_bits if qtype.has_size_in_bits else UNRESOLVED_SIZE,
        is_signed=signed,
        fraction_places=fraction_places,
    )
