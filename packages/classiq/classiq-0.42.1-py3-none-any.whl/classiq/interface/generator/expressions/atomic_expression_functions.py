from classiq.interface.generator.functions.classical_type import CLASSICAL_ATTRIBUTES

SUPPORTED_BUILTIN_FUNCTIONS = ["len", "sum", "print"]

SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS = {
    "do_subscript",
    "hypercube_entangler_graph",
    "grid_entangler_graph",
    "qft_const_adder_phase",
    "log_normal_finance_post_process",
    "gaussian_finance_post_process",
    "get_type",
    "struct_literal",
    "get_field",
    "molecule_problem_to_hamiltonian",
    "fock_hamiltonian_problem_to_hamiltonian",
    "molecule_ground_state_solution_post_process",
    "BitwiseAnd",
    "BitwiseXor",
    "BitwiseNot",
    "BitwiseOr",
    *SUPPORTED_BUILTIN_FUNCTIONS,
}

SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS_QMOD = (
    SUPPORTED_ATOMIC_EXPRESSION_FUNCTIONS - CLASSICAL_ATTRIBUTES
)
