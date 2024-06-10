import pydantic

from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
)
from classiq.interface.model.statement_block import StatementBlock
from classiq.interface.model.validations.handles_validator import HandleValidator
from classiq.interface.model.variable_declaration_statement import (
    VariableDeclarationStatement,
)

from classiq.exceptions import ClassiqValueError


class NativeFunctionDefinition(QuantumFunctionDeclaration):
    """
    Facilitates the creation of a user-defined composite function

    This class sets extra to forbid so that it can be used in a Union and not "steal"
    objects from other classes.
    """

    body: StatementBlock = pydantic.Field(
        default_factory=list, description="List of function calls to perform."
    )

    def validate_body(self) -> None:
        handle_validator = HandleValidator(self.port_declarations)

        for statement in self.body:
            if isinstance(statement, VariableDeclarationStatement):
                handle_validator.handle_variable_declaration(statement)
            else:
                handle_validator.handle_operation(statement)

        handle_validator.report_errored_handles(ClassiqValueError)
