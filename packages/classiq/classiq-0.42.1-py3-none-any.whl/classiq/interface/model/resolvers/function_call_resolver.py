import itertools
from typing import Any, Mapping

from classiq.interface.generator.visitor import Visitor
from classiq.interface.model.control import Control
from classiq.interface.model.invert import Invert
from classiq.interface.model.native_function_definition import NativeFunctionDefinition
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.repeat import Repeat
from classiq.interface.model.within_apply_operation import WithinApply


class FunctionCallResolver(Visitor):
    def __init__(
        self,
        quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
    ) -> None:
        self._quantum_function_dict = quantum_function_dict

    def visit_Invert(self, invert: Invert) -> None:
        for fc in invert.body:
            self.visit(fc)

    def visit_Repeat(self, repeat: Repeat) -> None:
        for fc in repeat.body:
            self.visit(fc)

    def visit_Control(self, control: Control) -> None:
        for fc in control.body:
            self.visit(fc)

    def visit_WithinApply(self, within_apply: WithinApply) -> None:
        for fc in itertools.chain(within_apply.compute, within_apply.action):
            self.visit(fc)

    def visit_QuantumFunctionCall(self, fc: QuantumFunctionCall) -> None:
        fc.resolve_function_decl(self._quantum_function_dict, check_operands=True)
        self.visit_BaseModel(fc)

    def visit_NativeFunctionDefinition(
        self, func_def: NativeFunctionDefinition
    ) -> None:
        curr_dict = self._quantum_function_dict
        self._quantum_function_dict = {
            **self._quantum_function_dict,
            **func_def.operand_declarations,
        }
        self.visit_BaseModel(func_def)
        self._quantum_function_dict = curr_dict


def resolve_function_calls(
    root: Any,
    quantum_function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    FunctionCallResolver(
        {
            **QuantumFunctionDeclaration.BUILTIN_FUNCTION_DECLARATIONS,
            **quantum_function_dict,
        },
    ).visit(root)
