import ast
from typing import Dict, List

from classiq.executor import DEFAULT_RESULT_NAME

STANDARD_CMAIN_BODY_LENGTH = 2  # assignment of sample call, save statement


class NonStandardClassicalCodeError(Exception):
    pass


# `is_standard_cmain` and `extract_sample_params` could easily be merged to one function, as they
# are doing similar tasks, but we decided to separate them for the sake of a better interface
def is_standard_cmain(model_classical_execution_code: str) -> bool:
    try:
        classical_body = _get_classical_body(model_classical_execution_code)
        if len(classical_body) != STANDARD_CMAIN_BODY_LENGTH:
            return False

        _assert_sample_call(classical_body)
        _assert_save_statement(classical_body)

        return True
    except NonStandardClassicalCodeError:
        return False


def extract_sample_params(model_classical_execution_code: str) -> Dict[str, float]:
    classical_main = _get_classical_body(model_classical_execution_code)

    qmain_params: Dict[str, float] = {}
    sample_call = _get_sample_call(classical_main)
    if len(sample_call.args) == 1 and isinstance(sample_call.args[0], ast.Dict):
        ast_dict = sample_call.args[0]
        qmain_params = dict(
            zip(
                [k.value for k in ast_dict.keys if isinstance(k, ast.Constant)],
                [v.value for v in ast_dict.values if isinstance(v, ast.Constant)],
            )
        )

    return qmain_params


def has_classical_exec(model_classical_execution_code: str) -> bool:
    return model_classical_execution_code != ""


def _get_classical_body(model_classical_execution_code: str) -> List[ast.stmt]:
    if not has_classical_exec(model_classical_execution_code):
        raise NonStandardClassicalCodeError
    return ast.parse(model_classical_execution_code).body


def _assert_sample_call(classical_body: List[ast.stmt]) -> None:
    _get_sample_call(classical_body)


def _get_sample_call(
    classical_body: List[ast.stmt],
) -> ast.Call:
    classical_call = classical_body[0]
    if not isinstance(classical_call, ast.Assign):
        raise NonStandardClassicalCodeError

    if len(classical_call.targets) != 1:
        raise NonStandardClassicalCodeError
    target = classical_call.targets[0]
    if not isinstance(target, ast.Name) or target.id != DEFAULT_RESULT_NAME:
        raise NonStandardClassicalCodeError

    invoked_expression = classical_call.value
    if not isinstance(invoked_expression, ast.Call):
        raise NonStandardClassicalCodeError
    if (
        not isinstance(invoked_expression.func, ast.Name)
        or invoked_expression.func.id != "sample"
    ):
        raise NonStandardClassicalCodeError

    return invoked_expression


def _assert_save_statement(classical_body: List[ast.stmt]) -> None:
    save_statement = classical_body[1]
    if not isinstance(save_statement, ast.Expr) or not isinstance(
        save_statement.value, ast.Call
    ):
        raise NonStandardClassicalCodeError

    call = save_statement.value
    if not isinstance(call.func, ast.Name) or call.func.id != "save":
        raise NonStandardClassicalCodeError

    if not len(call.args) == 1:
        raise NonStandardClassicalCodeError

    if (
        not isinstance(call.args[0], ast.Dict)
        or not isinstance(call.args[0].keys[0], ast.Constant)
        or call.args[0].keys[0].value != DEFAULT_RESULT_NAME
        or not isinstance(call.args[0].values[0], ast.Name)
        or call.args[0].values[0].id != DEFAULT_RESULT_NAME
    ):
        raise NonStandardClassicalCodeError
