from __future__ import annotations
import _jormungandr.autodiff
import typing
__all__ = ['EqualityConstraints', 'InequalityConstraints', 'OptimizationProblem', 'SolverExitCondition', 'SolverIterationInfo', 'SolverStatus']
M = typing.TypeVar("M", bound=int)
class EqualityConstraints:
    """
    A vector of equality constraints of the form cₑ(x) = 0.
    """
    def __bool__(self) -> bool:
        """
        Implicit conversion operator to bool.
        """
class InequalityConstraints:
    """
    A vector of inequality constraints of the form cᵢ(x) ≥ 0.
    """
    def __bool__(self) -> bool:
        """
        Implicit conversion operator to bool.
        """
class OptimizationProblem:
    """
    This class allows the user to pose a constrained nonlinear
    optimization problem in natural mathematical notation and solve it.
    
    This class supports problems of the form: @verbatim minₓ f(x) subject
    to cₑ(x) = 0 cᵢ(x) ≥ 0 @endverbatim
    
    where f(x) is the scalar cost function, x is the vector of decision
    variables (variables the solver can tweak to minimize the cost
    function), cᵢ(x) are the inequality constraints, and cₑ(x) are the
    equality constraints. Constraints are equations or inequalities of the
    decision variables that constrain what values the solver is allowed to
    use when searching for an optimal solution.
    
    The nice thing about this class is users don't have to put their
    system in the form shown above manually; they can write it in natural
    mathematical form and it'll be converted for them.
    """
    def __init__(self) -> None:
        """
        Construct the optimization problem.
        """
    def callback(self, callback: typing.Callable[[SolverIterationInfo], bool]) -> None:
        """
        Sets a callback to be called at each solver iteration.
        
        The callback for this overload should return bool.
        
        Parameter ``callback``:
            The callback. Returning true from the callback causes the solver
            to exit early with the solution it has so far.
        """
    @typing.overload
    def decision_variable(self) -> _jormungandr.autodiff.Variable:
        """
        Create a decision variable in the optimization problem.
        """
    @typing.overload
    def decision_variable(self, rows: int, cols: int = 1) -> _jormungandr.autodiff.VariableMatrix:
        """
        Create a matrix of decision variables in the optimization problem.
        
        Parameter ``rows``:
            Number of matrix rows.
        
        Parameter ``cols``:
            Number of matrix columns.
        """
    @typing.overload
    def maximize(self, objective: _jormungandr.autodiff.Variable) -> None:
        """
        Tells the solver to maximize the output of the given objective
        function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``objective``:
            The objective function to maximize.
        """
    @typing.overload
    def maximize(self, objective: _jormungandr.autodiff.VariableMatrix) -> None:
        """
        Tells the solver to maximize the output of the given objective
        function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``objective``:
            The objective function to maximize.
        """
    @typing.overload
    def maximize(self, objective: float) -> None:
        """
        Tells the solver to maximize the output of the given objective
        function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``objective``:
            The objective function to maximize.
        """
    @typing.overload
    def minimize(self, cost: _jormungandr.autodiff.Variable) -> None:
        """
        Tells the solver to minimize the output of the given cost function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``cost``:
            The cost function to minimize.
        """
    @typing.overload
    def minimize(self, cost: _jormungandr.autodiff.VariableMatrix) -> None:
        """
        Tells the solver to minimize the output of the given cost function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``cost``:
            The cost function to minimize.
        """
    @typing.overload
    def minimize(self, cost: float) -> None:
        """
        Tells the solver to minimize the output of the given cost function.
        
        Note that this is optional. If only constraints are specified, the
        solver will find the closest solution to the initial conditions that's
        in the feasible set.
        
        Parameter ``cost``:
            The cost function to minimize.
        """
    def solve(self, **kwargs) -> SolverStatus:
        """
        Solve the optimization problem. The solution will be stored in the
        original variables used to construct the problem.
        
        Parameter ``tolerance``:
            The solver will stop once the error is below this tolerance.
            (default: 1e-8)
        
        Parameter ``max_iterations``:
            The maximum number of solver iterations before returning a solution.
            (default: 5000)
        
        Parameter ``acceptable_tolerance``:
            The solver will stop once the error is below this tolerance for
            `acceptable_iterations` iterations. This is useful in cases where the
            solver might not be able to achieve the desired level of accuracy due to
            floating-point round-off.
            (default: 1e-6)
        
        Parameter ``max_acceptable_iterations``:
            The solver will stop once the error is below `acceptable_tolerance` for
            this many iterations.
            (default: 15)
        
        Parameter ``timeout``:
            The maximum elapsed wall clock time before returning a solution.
            (default: infinity)
        
        Parameter ``feasible_ipm``:
            Enables the feasible interior-point method. When the inequality
            constraints are all feasible, step sizes are reduced when necessary to
            prevent them becoming infeasible again. This is useful when parts of the
            problem are ill-conditioned in infeasible regions (e.g., square root of a
            negative value). This can slow or prevent progress toward a solution
            though, so only enable it if necessary.
            (default: False)
        
        Parameter ``diagnostics``:
            Enables diagnostic prints.
            (default: False)
        
        Parameter ``spy``:
            Enables writing sparsity patterns of H, Aₑ, and Aᵢ to files named H.spy,
            A_e.spy, and A_i.spy respectively during solve.
        
            Use tools/spy.py to plot them.
            (default: False)
        """
    @typing.overload
    def subject_to(self, constraint: EqualityConstraints) -> None:
        """
        Tells the solver to solve the problem while satisfying the given
        equality constraint.
        
        Parameter ``constraint``:
            The constraint to satisfy.
        """
    @typing.overload
    def subject_to(self, constraint: InequalityConstraints) -> None:
        """
        Tells the solver to solve the problem while satisfying the given
        inequality constraint.
        
        Parameter ``constraint``:
            The constraint to satisfy.
        """
    def symmetric_decision_variable(self, rows: int) -> _jormungandr.autodiff.VariableMatrix:
        """
        Create a symmetric matrix of decision variables in the optimization
        problem.
        
        Variable instances are reused across the diagonal, which helps reduce
        problem dimensionality.
        
        Parameter ``rows``:
            Number of matrix rows.
        """
class SolverExitCondition:
    """
    Solver exit condition.
    
    Members:
    
      SUCCESS : Solved the problem to the desired tolerance.
    
      SOLVED_TO_ACCEPTABLE_TOLERANCE : Solved the problem to an acceptable tolerance, but not the desired
    one.
    
      CALLBACK_REQUESTED_STOP : The solver returned its solution so far after the user requested a
    stop.
    
      TOO_FEW_DOFS : The solver determined the problem to be overconstrained and gave up.
    
      LOCALLY_INFEASIBLE : The solver determined the problem to be locally infeasible and gave
    up.
    
      FEASIBILITY_RESTORATION_FAILED : The solver failed to reach the desired tolerance, and feasibility
    restoration failed to converge.
    
      NONFINITE_INITIAL_COST_OR_CONSTRAINTS : The solver encountered nonfinite initial cost or constraints and gave
    up.
    
      DIVERGING_ITERATES : The solver encountered diverging primal iterates xₖ and/or sₖ and gave
    up.
    
      MAX_ITERATIONS_EXCEEDED : The solver returned its solution so far after exceeding the maximum
    number of iterations.
    
      TIMEOUT : The solver returned its solution so far after exceeding the maximum
    elapsed wall clock time.
    """
    CALLBACK_REQUESTED_STOP: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.CALLBACK_REQUESTED_STOP: 2>
    DIVERGING_ITERATES: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.DIVERGING_ITERATES: -5>
    FEASIBILITY_RESTORATION_FAILED: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.FEASIBILITY_RESTORATION_FAILED: -3>
    LOCALLY_INFEASIBLE: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.LOCALLY_INFEASIBLE: -2>
    MAX_ITERATIONS_EXCEEDED: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.MAX_ITERATIONS_EXCEEDED: -6>
    NONFINITE_INITIAL_COST_OR_CONSTRAINTS: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.NONFINITE_INITIAL_COST_OR_CONSTRAINTS: -4>
    SOLVED_TO_ACCEPTABLE_TOLERANCE: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.SOLVED_TO_ACCEPTABLE_TOLERANCE: 1>
    SUCCESS: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.SUCCESS: 0>
    TIMEOUT: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.TIMEOUT: -7>
    TOO_FEW_DOFS: typing.ClassVar[SolverExitCondition]  # value = <SolverExitCondition.TOO_FEW_DOFS: -1>
    __members__: typing.ClassVar[dict[str, SolverExitCondition]]  # value = {'SUCCESS': <SolverExitCondition.SUCCESS: 0>, 'SOLVED_TO_ACCEPTABLE_TOLERANCE': <SolverExitCondition.SOLVED_TO_ACCEPTABLE_TOLERANCE: 1>, 'CALLBACK_REQUESTED_STOP': <SolverExitCondition.CALLBACK_REQUESTED_STOP: 2>, 'TOO_FEW_DOFS': <SolverExitCondition.TOO_FEW_DOFS: -1>, 'LOCALLY_INFEASIBLE': <SolverExitCondition.LOCALLY_INFEASIBLE: -2>, 'FEASIBILITY_RESTORATION_FAILED': <SolverExitCondition.FEASIBILITY_RESTORATION_FAILED: -3>, 'NONFINITE_INITIAL_COST_OR_CONSTRAINTS': <SolverExitCondition.NONFINITE_INITIAL_COST_OR_CONSTRAINTS: -4>, 'DIVERGING_ITERATES': <SolverExitCondition.DIVERGING_ITERATES: -5>, 'MAX_ITERATIONS_EXCEEDED': <SolverExitCondition.MAX_ITERATIONS_EXCEEDED: -6>, 'TIMEOUT': <SolverExitCondition.TIMEOUT: -7>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SolverIterationInfo:
    """
    Solver iteration information exposed to a user callback.
    """
    @property
    def A_e(self) -> scipy.sparse.csc_matrix:
        """
        The equality constraint Jacobian.
        """
    @property
    def A_i(self) -> scipy.sparse.csc_matrix:
        """
        The inequality constraint Jacobian.
        """
    @property
    def H(self) -> scipy.sparse.csc_matrix:
        """
        The Hessian of the Lagrangian.
        """
    @property
    def g(self) -> scipy.sparse.csc_matrix:
        """
        The gradient of the cost function.
        """
    @property
    def iteration(self) -> int:
        """
        The solver iteration.
        """
    @property
    def x(self) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        The decision variables.
        """
class SolverStatus:
    """
    Return value of OptimizationProblem::Solve() containing the cost
    function and constraint types and solver's exit condition.
    """
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, cost_function_type: _jormungandr.autodiff.ExpressionType = ..., equality_constraint_type: _jormungandr.autodiff.ExpressionType = ..., inequality_constraint_type: _jormungandr.autodiff.ExpressionType = ..., exit_condition: SolverExitCondition = ..., cost: float = 0.0) -> None:
        ...
    @property
    def cost(self) -> float:
        """
        The solution's cost.
        """
    @cost.setter
    def cost(self, arg0: float) -> None:
        ...
    @property
    def cost_function_type(self) -> _jormungandr.autodiff.ExpressionType:
        """
        The cost function type detected by the solver.
        """
    @cost_function_type.setter
    def cost_function_type(self, arg0: _jormungandr.autodiff.ExpressionType) -> None:
        ...
    @property
    def equality_constraint_type(self) -> _jormungandr.autodiff.ExpressionType:
        """
        The equality constraint type detected by the solver.
        """
    @equality_constraint_type.setter
    def equality_constraint_type(self, arg0: _jormungandr.autodiff.ExpressionType) -> None:
        ...
    @property
    def exit_condition(self) -> SolverExitCondition:
        """
        The solver's exit condition.
        """
    @exit_condition.setter
    def exit_condition(self, arg0: SolverExitCondition) -> None:
        ...
    @property
    def inequality_constraint_type(self) -> _jormungandr.autodiff.ExpressionType:
        """
        The inequality constraint type detected by the solver.
        """
    @inequality_constraint_type.setter
    def inequality_constraint_type(self, arg0: _jormungandr.autodiff.ExpressionType) -> None:
        ...
