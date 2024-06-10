from typing import Dict, Mapping, Set, Union

from classiq.interface.generator.function_params import PortDirection
from classiq.interface.generator.functions.builtins.quantum_operators import (
    APPLY_OPERATOR,
)
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.port_declaration import PortDeclaration
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_statement import QuantumOperation
from classiq.interface.model.statement_block import StatementBlock
from classiq.interface.model.validation_handle import HandleState, ValidationHandle
from classiq.interface.model.validations.handle_validation_base import (
    HandleValidationBase,
)
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)
from classiq.interface.model.within_apply_operation import WithinApply

from classiq.exceptions import ClassiqValueError


def _initialize_handles_to_state(
    port_declarations: Mapping[str, PortDeclaration],
) -> Dict[str, ValidationHandle]:
    handles_to_state: Dict[str, ValidationHandle] = dict()

    for port_decl in port_declarations.values():
        handles_to_state[port_decl.name] = ValidationHandle(
            initial_state=(
                HandleState.INITIALIZED
                if port_decl.direction.includes_port_direction(PortDirection.Input)
                else HandleState.UNINITIALIZED
            )
        )

    return handles_to_state


class HandleValidator(HandleValidationBase):
    def __init__(
        self,
        port_declarations: Mapping[str, PortDeclaration],
    ) -> None:
        super().__init__(port_declarations)
        self._port_declarations = port_declarations.values()
        self._handles_to_state = _initialize_handles_to_state(port_declarations)

    @property
    def _validation_handles_state(self) -> Mapping[str, ValidationHandle]:
        return self._handles_to_state

    def handle_operation(self, op: QuantumOperation) -> None:
        if isinstance(op, QuantumFunctionCall) and op.function == APPLY_OPERATOR.name:
            call_name = op.operands[APPLY_OPERATOR.operand_names[0]]
            self._handle_apply([QuantumFunctionCall(function=call_name)])
        elif isinstance(op, WithinApply):
            self._handle_apply(op.action)

        self._handle_inputs(op.wiring_inputs)
        self._handle_outputs(op.wiring_outputs)
        self._handle_inouts(op.wiring_inouts)

    def handle_variable_declaration(
        self, declaration: VariableDeclarationStatement
    ) -> None:
        handle_wiring_state = self._handles_to_state.get(declaration.name)
        if handle_wiring_state is not None:
            handle_wiring_state.append_error(
                f"Trying to declare a variable of the same name as previously declared variable {declaration.name}"
            )
            return

        self._handles_to_state[declaration.name] = ValidationHandle(
            HandleState.UNINITIALIZED
        )

    def _handle_inputs(self, inputs: Mapping[str, HandleBinding]) -> None:
        for handle_binding in inputs.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]
            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name!r} as input but it is in incorrect state"
                )
                continue

            handle_wiring_state.uninitialize()

    def _handle_outputs(self, outputs: Mapping[str, HandleBinding]) -> None:
        for handle_binding in outputs.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.UNINITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name!r} as output but it is in incorrect state"
                )
                continue

            handle_wiring_state.initialize()

    def _handle_inouts(
        self,
        inouts: Mapping[
            str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
        ],
    ) -> None:
        sliced_handles = set()
        whole_handles = set()

        for handle_binding in inouts.values():
            handle_wiring_state = self._handles_to_state[handle_binding.name]

            if handle_wiring_state.state is not HandleState.INITIALIZED:
                handle_wiring_state.append_error(
                    f"Trying to access handle {handle_binding.name!r} as inout but it is in incorrect state"
                )

            if isinstance(
                handle_binding, (SlicedHandleBinding, SubscriptHandleBinding)
            ):
                sliced_handles.add(handle_binding.name)
            else:
                whole_handles.add(handle_binding.name)

        for handle in sliced_handles & whole_handles:
            self._handles_to_state[handle].append_error(
                f"Invalid use of inout handle {handle!r}, used both in slice or subscript and whole"
            )

    def _handle_apply(self, body: StatementBlock) -> None:
        local_variables: Set[str] = set()
        output_capturing_variables: Set[str] = set()
        for statement in body:
            if isinstance(statement, VariableDeclarationStatement):
                local_variables.add(statement.name)
            elif isinstance(statement, QuantumOperation):
                for handle in statement.wiring_outputs.values():
                    if (
                        handle.name in local_variables
                        or handle.name in output_capturing_variables
                    ):
                        continue
                    output_capturing_variables.add(handle.name)
                    self._handles_to_state[handle.name].initialize()
            else:
                raise ClassiqValueError(
                    f"Unknown statement type {type(statement).__name__}"
                )
