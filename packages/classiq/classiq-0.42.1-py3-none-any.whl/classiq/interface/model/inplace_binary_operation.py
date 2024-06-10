from typing import Literal, Mapping

import pydantic

from classiq.interface.helpers.pydantic_model_helpers import nameables_to_dict
from classiq.interface.model.handle_binding import HandleBinding
from classiq.interface.model.quantum_statement import QuantumOperation

from classiq._internals.enum_utils import StrEnum
from classiq.exceptions import ClassiqValueError


class BinaryOperation(StrEnum):
    Addition = "inplace_add"
    Xor = "inplace_xor"

    @property
    def internal_function(self) -> str:
        return {
            BinaryOperation.Addition: "modular_add",
            BinaryOperation.Xor: "integer_xor",
        }[self]


class InplaceBinaryOperation(QuantumOperation):
    kind: Literal["InplaceBinaryOperation"]

    target: HandleBinding
    value: HandleBinding
    operation: BinaryOperation

    @property
    def wiring_inouts(self) -> Mapping[str, HandleBinding]:
        return nameables_to_dict([self.target, self.value])

    @pydantic.validator("target", "value")
    def validate_handle(cls, handle: HandleBinding) -> HandleBinding:
        if not handle.is_bindable():
            raise ClassiqValueError(f"Cannot bind '{handle!r}'")
        return handle
