# This file was generated automatically - do not edit manually

from classiq.interface.generator.expressions.enums.ladder_operator import LadderOperator
from classiq.interface.generator.expressions.enums.pauli import Pauli

from classiq.qmod.qmod_parameter import CArray, CBool, CInt, CReal
from classiq.qmod.qmod_struct import struct


@struct
class PauliTerm:
    pauli: CArray[Pauli]
    coefficient: CReal


@struct
class MoleculeProblem:
    mapping: CInt
    z2_symmetries: CBool
    molecule: "Molecule"
    freeze_core: CBool
    remove_orbitals: CArray[CInt]


@struct
class Molecule:
    atoms: CArray["ChemistryAtom"]
    spin: CInt
    charge: CInt


@struct
class ChemistryAtom:
    element: CInt
    position: "Position"


@struct
class Position:
    x: CReal
    y: CReal
    z: CReal


@struct
class FockHamiltonianProblem:
    mapping: CInt
    z2_symmetries: CBool
    terms: CArray["LadderTerm"]
    num_particles: CArray[CInt]


@struct
class LadderTerm:
    coefficient: CReal
    ops: CArray["LadderOp"]


@struct
class LadderOp:
    op: LadderOperator
    index: CInt


@struct
class CombinatorialOptimizationSolution:
    probability: CReal
    cost: CReal
    solution: CArray[CInt]
    count: CInt


@struct
class GaussianModel:
    num_qubits: CInt
    normal_max_value: CReal
    default_probabilities: CArray[CReal]
    rhos: CArray[CReal]
    loss: CArray[CInt]
    min_loss: CInt


@struct
class LogNormalModel:
    num_qubits: CInt
    mu: CReal
    sigma: CReal


@struct
class FinanceFunction:
    f: CInt
    threshold: CReal
    larger: CBool
    polynomial_degree: CInt
    use_chebyshev_polynomial_approximation: CBool
    tail_probability: CReal


@struct
class QsvmResult:
    test_score: CReal
    predicted_labels: CArray[CReal]


@struct
class QSVMFeatureMapPauli:
    feature_dimension: CInt
    reps: CInt
    entanglement: CInt
    alpha: CReal
    paulis: CArray[CArray[Pauli]]


__all__ = [
    "PauliTerm",
    "MoleculeProblem",
    "Molecule",
    "ChemistryAtom",
    "Position",
    "FockHamiltonianProblem",
    "LadderTerm",
    "LadderOp",
    "CombinatorialOptimizationSolution",
    "GaussianModel",
    "LogNormalModel",
    "FinanceFunction",
    "QsvmResult",
    "QSVMFeatureMapPauli",
]
