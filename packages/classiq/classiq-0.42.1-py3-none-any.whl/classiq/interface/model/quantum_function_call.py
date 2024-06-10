import itertools
import re
from typing import Any, Dict, List, Literal, Mapping, Optional, Set, Type, Union

import pydantic

from classiq.interface.ast_node import ASTNode
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.functions.function_declaration import (
    FunctionDeclaration,
)
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_lambda_function import (
    QuantumCallable,
    QuantumLambdaFunction,
    QuantumOperand,
)
from classiq.interface.model.quantum_statement import QuantumOperation
from classiq.interface.model.validation_handle import get_unique_handle_names

from classiq.exceptions import ClassiqError, ClassiqValueError


def _validate_no_duplicated_ports(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = inputs.keys() & inouts.keys()
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as ports in both inputs and inouts"
        )

    outputs_and_inouts = outputs.keys() & inouts.keys()
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as ports in both outputs and inouts"
        )


def _validate_no_duplicated_handles(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = get_unique_handle_names(inputs) & get_unique_handle_names(
        inouts
    )
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as handles in both inputs and inouts"
        )

    outputs_and_inouts = get_unique_handle_names(outputs) & get_unique_handle_names(
        inouts
    )
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as handles in both outputs and inouts"
        )


def _validate_no_mixing_sliced_and_whole_handles(
    inouts: Mapping[str, HandleBinding],
) -> None:
    def _treat_subscript_as_slice(type_: Type[HandleBinding]) -> Type[HandleBinding]:
        if type_ == SubscriptHandleBinding:
            return SlicedHandleBinding
        return type_

    inout_handle_names_to_types = {
        handle_name: {_treat_subscript_as_slice(type(handle)) for handle in handles}
        for handle_name, handles in itertools.groupby(
            inouts.values(), lambda handle: handle.name
        )
    }
    invalid_handles = [
        handle
        for handle, types in inout_handle_names_to_types.items()
        if len(types) > 1
    ]
    if invalid_handles:
        raise ClassiqValueError(
            f"Inout handles {', '.join(invalid_handles)} mix sliced and whole handles"
        )


ArgValue = Union[
    Expression,
    QuantumOperand,
    SlicedHandleBinding,
    SubscriptHandleBinding,
    HandleBinding,
]


class OperandIdentifier(ASTNode):
    name: str
    index: Expression


class QuantumFunctionCall(QuantumOperation):
    kind: Literal["QuantumFunctionCall"]

    function: Union[str, OperandIdentifier] = pydantic.Field(
        description="The function that is called"
    )
    params: Dict[str, Expression] = pydantic.Field(default_factory=dict)
    inputs: Dict[str, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the wire it connects to",
    )
    inouts: Dict[
        str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    ] = pydantic.Field(
        default_factory=dict,
        description="A mapping from in/out name to the wires that connect to it",
    )
    outputs: Dict[str, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the wire it connects to",
    )
    operands: Dict[str, QuantumOperand] = pydantic.Field(
        description="Function calls passed to the operator",
        default_factory=dict,
    )
    positional_args: List[ArgValue] = pydantic.Field(default_factory=list)

    _func_decl: Optional[QuantumFunctionDeclaration] = pydantic.PrivateAttr(
        default=None
    )

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        if self._func_decl is None:
            raise ClassiqError("Accessing an unresolved quantum function call")

        return self._func_decl

    def set_func_decl(self, fd: Optional[FunctionDeclaration]) -> None:
        if fd is not None and not isinstance(fd, QuantumFunctionDeclaration):
            raise ClassiqValueError(
                "the declaration of a quantum function call cannot be set to a non-quantum function declaration."
            )
        self._func_decl = fd

    @property
    def func_name(self) -> str:
        if isinstance(self.function, OperandIdentifier):
            return self.function.name
        return self.function

    @property
    def wiring_inputs(self) -> Mapping[str, HandleBinding]:
        return self.inputs

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[
        str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    ]:
        return self.inouts

    @property
    def wiring_outputs(self) -> Mapping[str, HandleBinding]:
        return self.outputs

    def get_positional_args(self) -> List[ArgValue]:
        result: List[ArgValue] = self.positional_args
        if not result:
            result = list(self.params.values())
            result.extend(self.operands.values())
            result.extend(self.inputs.values())
            result.extend(self.inouts.values())
            result.extend(self.outputs.values())
        return result

    @property
    def pos_param_args(self) -> Dict[str, Expression]:
        return dict(
            zip(
                self.func_decl.param_decls.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, Expression)
                ),
            )
        )

    @property
    def pos_operand_args(self) -> Dict[str, "QuantumOperand"]:
        return dict(
            zip(
                self.func_decl.operand_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if not isinstance(param, (Expression, HandleBinding))
                ),
            )
        )

    @property
    def pos_port_args(self) -> Dict[str, HandleBinding]:
        return dict(
            zip(
                self.func_decl.port_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, HandleBinding)
                ),
            )
        )

    def _update_pos_port_params(self) -> None:
        for name, port_decl in self.func_decl.port_declarations.items():
            if port_decl.direction == PortDeclarationDirection.Input:
                self.inputs[name] = self.pos_port_args[name]
            elif port_decl.direction == PortDeclarationDirection.Output:
                self.outputs[name] = self.pos_port_args[name]
            else:
                self.inouts[name] = self.pos_port_args[name]

    def _reduce_positional_args_to_keywords(self) -> None:
        self.params.update(self.pos_param_args)
        self.operands.update(self.pos_operand_args)
        self._update_pos_port_params()

    def resolve_function_decl(
        self,
        function_dict: Mapping[str, QuantumFunctionDeclaration],
        check_operands: bool,
    ) -> None:
        if self._func_decl is None:
            func_decl = function_dict.get(self.func_name)
            if func_decl is None:
                raise ClassiqValueError(
                    f"Error resolving function {self.func_name}, the function is not found in included library."
                )
            self.set_func_decl(func_decl)

        if self.positional_args:
            self._reduce_positional_args_to_keywords()

        _check_params_against_declaration(
            set(self.params.keys()),
            set(self.func_decl.param_decls.keys()),
            self.func_decl.name,
        )
        _check_ports_against_declaration(self, self.func_decl)
        _check_params_against_declaration(
            set(self.operands.keys()),
            set(self.func_decl.operand_declarations.keys()),
            self.func_name,
        )
        if check_operands:
            _check_operands_against_declaration(self, self.func_decl, function_dict)

        for name, op in self.operands.items():
            op_decl = self.func_decl.operand_declarations[name]
            for qlambda in get_lambda_defs(op):
                if isinstance(qlambda, QuantumLambdaFunction):
                    qlambda.set_op_decl(op_decl)

    @pydantic.root_validator()
    def validate_handles(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        inputs = values.get("inputs", dict())
        outputs = values.get("outputs", dict())
        inouts = values.get("inouts", dict())

        _validate_no_duplicated_ports(inputs, outputs, inouts)
        _validate_no_duplicated_handles(inputs, outputs, inouts)
        _validate_no_mixing_sliced_and_whole_handles(inouts)

        return values


def get_lambda_defs(operand: QuantumOperand) -> List[QuantumCallable]:
    if isinstance(operand, list):
        return operand
    return [operand]


def _check_ports_against_declaration(
    call: QuantumFunctionCall, decl: QuantumFunctionDeclaration
) -> None:
    call_input_names = set(call.inputs.keys())

    _check_params_against_declaration(
        call_input_names,
        decl.ports_by_declaration_direction(PortDeclarationDirection.Input),
        call.func_name,
    )

    call_output_names = set(call.outputs.keys())

    _check_params_against_declaration(
        call_output_names,
        decl.ports_by_declaration_direction(PortDeclarationDirection.Output),
        call.func_name,
    )

    inout_params = set(call.inouts.keys())

    _check_params_against_declaration(
        inout_params,
        decl.ports_by_declaration_direction(PortDeclarationDirection.Inout),
        call.func_name,
    )


def _check_operand_against_declaration(
    call: QuantumFunctionCall,
    operand_decl: QuantumOperandDeclaration,
    operand_argument: QuantumOperand,
    function_dict: Mapping[str, QuantumFunctionDeclaration],
    in_list: bool = False,
) -> None:
    if isinstance(operand_argument, list):
        if in_list:
            raise ClassiqValueError(
                f"{str(operand_argument)!r} argument to {call.func_decl.name!r} is not "
                f"a valid operand. Nested operand lists are not permitted"
            )
        for arg in operand_argument:
            _check_operand_against_declaration(
                call, operand_decl, arg, function_dict, in_list=True
            )
        return
    operand_arg_decl: QuantumFunctionDeclaration
    if isinstance(operand_argument, str):
        if operand_argument not in function_dict:
            raise ClassiqValueError(
                f"{operand_argument!r} argument to {call.func_decl.name!r} is not a "
                f"registered function"
            )
        operand_arg_decl = function_dict[operand_argument]
    elif isinstance(operand_argument, QuantumLambdaFunction):
        if operand_argument.func_decl is None:
            return
        operand_arg_decl = operand_argument.func_decl
    else:
        raise ClassiqValueError(
            f"{str(operand_argument)!r} argument to {call.func_decl.name!r} is not a "
            f"valid operand"
        )
    num_arg_parameters = len(operand_arg_decl.get_positional_arg_decls())
    num_decl_parameters = len(operand_decl.get_positional_arg_decls())
    if num_arg_parameters != num_decl_parameters:
        raise ClassiqValueError(
            f"Signature of argument {operand_argument!r} to {call.func_decl.name!r} "
            f"does not match the signature of parameter {operand_decl.name!r}. "
            f"{operand_decl.name!r} accepts {num_decl_parameters} parameters but "
            f"{operand_argument!r} accepts {num_arg_parameters} parameters"
        )


def _check_operands_against_declaration(
    call: QuantumFunctionCall,
    decl: QuantumFunctionDeclaration,
    function_dict: Mapping[str, QuantumFunctionDeclaration],
) -> None:
    for operand_parameter, operand_argument in call.operands.items():
        _check_operand_against_declaration(
            call,
            decl.operand_declarations[operand_parameter],
            operand_argument,
            function_dict,
        )


def _check_params_against_declaration(
    call_params: Set[str],
    param_decls: Set[str],
    callee_name: str,
) -> None:
    unknown_params = call_params - param_decls
    if any(re.match(r"arg\d+", param) for param in unknown_params):
        error_msg = (
            f"Unsupported passing of named function {callee_name!r} as an operand."
            "\nSuggestion: replace the named function with lambda function."
        )
    else:
        error_msg = f"Unknown parameters {unknown_params} in call to {callee_name!r}."
    if unknown_params:
        raise ClassiqValueError(error_msg)

    missing_params = param_decls - call_params
    if missing_params:
        raise ClassiqValueError(
            f"Missing parameters {missing_params} in call to {callee_name!r}."
        )
