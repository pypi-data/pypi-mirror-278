from __future__ import annotations
import _jormungandr.optimization
import typing
__all__ = ['ExpressionType', 'Gradient', 'Hessian', 'Jacobian', 'Variable', 'VariableBlock', 'VariableMatrix', 'abs', 'acos', 'asin', 'atan', 'atan2', 'block', 'cos', 'cosh', 'cwise_reduce', 'erf', 'exp', 'hypot', 'log', 'log10', 'pow', 'sign', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
M = typing.TypeVar("M", bound=int)
N = typing.TypeVar("N", bound=int)
class ExpressionType:
    """
    Expression type.
    
    Used for autodiff caching.
    
    Members:
    
      NONE : There is no expression.
    
      CONSTANT : The expression is a constant.
    
      LINEAR : The expression is composed of linear and lower-order operators.
    
      QUADRATIC : The expression is composed of quadratic and lower-order operators.
    
      NONLINEAR : The expression is composed of nonlinear and lower-order operators.
    """
    CONSTANT: typing.ClassVar[ExpressionType]  # value = <ExpressionType.CONSTANT: 1>
    LINEAR: typing.ClassVar[ExpressionType]  # value = <ExpressionType.LINEAR: 2>
    NONE: typing.ClassVar[ExpressionType]  # value = <ExpressionType.NONE: 0>
    NONLINEAR: typing.ClassVar[ExpressionType]  # value = <ExpressionType.NONLINEAR: 4>
    QUADRATIC: typing.ClassVar[ExpressionType]  # value = <ExpressionType.QUADRATIC: 3>
    __members__: typing.ClassVar[dict[str, ExpressionType]]  # value = {'NONE': <ExpressionType.NONE: 0>, 'CONSTANT': <ExpressionType.CONSTANT: 1>, 'LINEAR': <ExpressionType.LINEAR: 2>, 'QUADRATIC': <ExpressionType.QUADRATIC: 3>, 'NONLINEAR': <ExpressionType.NONLINEAR: 4>}
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
class Gradient:
    """
    This class calculates the gradient of a a variable with respect to a
    vector of variables.
    
    The gradient is only recomputed if the variable expression is
    quadratic or higher order.
    """
    @typing.overload
    def __init__(self, variable: Variable, wrt: Variable) -> None:
        """
        Constructs a Gradient object.
        
        Parameter ``variable``:
            Variable of which to compute the gradient.
        
        Parameter ``wrt``:
            Variable with respect to which to compute the gradient.
        """
    @typing.overload
    def __init__(self, variable: Variable, wrt: VariableMatrix) -> None:
        """
        Constructs a Gradient object.
        
        Parameter ``variable``:
            Variable of which to compute the gradient.
        
        Parameter ``wrt``:
            Vector of variables with respect to which to compute the gradient.
        """
    def get(self) -> VariableMatrix:
        """
        Returns the gradient as a VariableMatrix.
        
        This is useful when constructing optimization problems with
        derivatives in them.
        """
    def update(self) -> None:
        """
        Updates the value of the variable.
        """
    def value(self) -> scipy.sparse.csc_matrix:
        """
        Evaluates the gradient at wrt's value.
        """
class Hessian:
    """
    This class calculates the Hessian of a variable with respect to a
    vector of variables.
    
    The gradient tree is cached so subsequent Hessian calculations are
    faster, and the Hessian is only recomputed if the variable expression
    is nonlinear.
    """
    def __init__(self, variable: Variable, wrt: VariableMatrix) -> None:
        """
        Constructs a Hessian object.
        
        Parameter ``variable``:
            Variable of which to compute the Hessian.
        
        Parameter ``wrt``:
            Vector of variables with respect to which to compute the Hessian.
        """
    def get(self) -> VariableMatrix:
        """
        Returns the Hessian as a VariableMatrix.
        
        This is useful when constructing optimization problems with
        derivatives in them.
        """
    def update(self) -> None:
        """
        Updates the values of the gradient tree.
        """
    def value(self) -> scipy.sparse.csc_matrix:
        """
        Evaluates the Hessian at wrt's value.
        """
class Jacobian:
    """
    This class calculates the Jacobian of a vector of variables with
    respect to a vector of variables.
    
    The Jacobian is only recomputed if the variable expression is
    quadratic or higher order.
    """
    def __init__(self, variables: VariableMatrix, wrt: VariableMatrix) -> None:
        """
        Constructs a Jacobian object.
        
        Parameter ``variables``:
            Vector of variables of which to compute the Jacobian.
        
        Parameter ``wrt``:
            Vector of variables with respect to which to compute the Jacobian.
        """
    def get(self) -> VariableMatrix:
        """
        Returns the Jacobian as a VariableMatrix.
        
        This is useful when constructing optimization problems with
        derivatives in them.
        """
    def update(self) -> None:
        """
        Updates the values of the variables.
        """
    def value(self) -> scipy.sparse.csc_matrix:
        """
        Evaluates the Jacobian at wrt's value.
        """
class Variable:
    """
    An autodiff variable pointing to an expression node.
    """
    __hash__: typing.ClassVar[None] = None
    @typing.overload
    def __add__(self, rhs: float) -> Variable:
        ...
    @typing.overload
    def __add__(self, rhs: Variable) -> Variable:
        ...
    @typing.overload
    def __eq__(self, rhs: Variable) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __iadd__(self, rhs: float) -> Variable:
        """
        Variable-Variable compound addition operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __iadd__(self, rhs: Variable) -> Variable:
        """
        Variable-Variable compound addition operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __imul__(self, rhs: float) -> Variable:
        """
        Variable-Variable compound multiplication operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __imul__(self, rhs: Variable) -> Variable:
        """
        Variable-Variable compound multiplication operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs a linear Variable with a value of zero.
        """
    @typing.overload
    def __init__(self, value: float) -> None:
        """
        Constructs a Variable from a double.
        
        Parameter ``value``:
            The value of the Variable.
        """
    @typing.overload
    def __init__(self, value: int) -> None:
        """
        Constructs a Variable from an int.
        
        Parameter ``value``:
            The value of the Variable.
        """
    @typing.overload
    def __isub__(self, rhs: float) -> Variable:
        """
        Variable-Variable compound subtraction operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __isub__(self, rhs: Variable) -> Variable:
        """
        Variable-Variable compound subtraction operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __itruediv__(self, rhs: float) -> Variable:
        """
        Variable-Variable compound division operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __itruediv__(self, rhs: Variable) -> Variable:
        """
        Variable-Variable compound division operator.
        
        Parameter ``rhs``:
            Operator right-hand side.
        """
    @typing.overload
    def __le__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __mul__(self, rhs: float) -> Variable:
        ...
    @typing.overload
    def __mul__(self, rhs: Variable) -> Variable:
        ...
    def __neg__(self) -> Variable:
        ...
    def __pos__(self) -> Variable:
        ...
    def __pow__(self, power: int) -> Variable:
        ...
    def __radd__(self, lhs: float) -> Variable:
        ...
    def __rmul__(self, lhs: float) -> Variable:
        ...
    def __rsub__(self, lhs: float) -> Variable:
        ...
    def __rtruediv__(self, lhs: float) -> Variable:
        ...
    @typing.overload
    def __sub__(self, rhs: float) -> Variable:
        ...
    @typing.overload
    def __sub__(self, rhs: Variable) -> Variable:
        ...
    @typing.overload
    def __truediv__(self, rhs: float) -> Variable:
        ...
    @typing.overload
    def __truediv__(self, rhs: Variable) -> Variable:
        ...
    @typing.overload
    def set_value(self, value: float) -> Variable:
        """
        Sets Variable's internal value.
        
        Parameter ``value``:
            The value of the Variable.
        """
    @typing.overload
    def set_value(self, value: int) -> Variable:
        """
        Sets Variable's internal value.
        
        Parameter ``value``:
            The value of the Variable.
        """
    def type(self) -> ExpressionType:
        """
        Returns the type of this expression (constant, linear, quadratic, or
        nonlinear).
        """
    def update(self) -> None:
        """
        Updates the value of this variable based on the values of its
        dependent variables.
        """
    def value(self) -> float:
        """
        Returns the value of this variable.
        """
class VariableBlock:
    """
    A submatrix of autodiff variables with reference semantics.
    
    Template parameter ``Mat``:
        The type of the matrix whose storage this class points to.
    """
    __hash__: typing.ClassVar[None] = None
    @typing.overload
    def __add__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self, rhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], rhs: VariableBlock) -> VariableMatrix:
        ...
    def __array_ufunc__(self, ufunc: typing.Any, method: str, *args, **kwargs) -> typing.Any:
        ...
    @typing.overload
    def __eq__(self, rhs: VariableMatrix) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: VariableBlock) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: Variable) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: int) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: Variable) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: int) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __getitem__(self, row: int) -> Variable:
        """
        Returns a scalar subblock at the given row.
        
        Parameter ``row``:
            The scalar subblock's row.
        """
    @typing.overload
    def __getitem__(self, slices: tuple) -> typing.Any:
        """
        Returns a scalar subblock at the given row and column.
        
        Parameter ``row``:
            The scalar subblock's row.
        
        Parameter ``col``:
            The scalar subblock's column.
        """
    @typing.overload
    def __gt__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __init__(self, mat: VariableMatrix) -> None:
        """
        Constructs a Variable block pointing to all of the given matrix.
        
        Parameter ``mat``:
            The matrix to which to point.
        """
    @typing.overload
    def __init__(self, mat: VariableMatrix, row_offset: int, col_offset: int, block_rows: int, block_cols: int) -> None:
        """
        Constructs a Variable block pointing to a subset of the given matrix.
        
        Parameter ``mat``:
            The matrix to which to point.
        
        Parameter ``row_offset``:
            The block's row offset.
        
        Parameter ``col_offset``:
            The block's column offset.
        
        Parameter ``block_rows``:
            The number of rows in the block.
        
        Parameter ``block_cols``:
            The number of columns in the block.
        """
    def __iter__(self) -> typing.Iterator[Variable]:
        ...
    @typing.overload
    def __le__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    def __len__(self) -> int:
        """
        Returns number of rows in the matrix.
        """
    @typing.overload
    def __lt__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    def __matmul__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: float) -> VariableMatrix:
        ...
    def __neg__(self) -> VariableMatrix:
        ...
    def __pow__(self, power: int) -> Variable:
        ...
    @typing.overload
    def __rmul__(self, lhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, lhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, lhs: float) -> VariableMatrix:
        ...
    @typing.overload
    def __setitem__(self, row: int, value: Variable) -> Variable:
        ...
    @typing.overload
    def __setitem__(self, slices: tuple, value: typing.Any) -> None:
        ...
    @typing.overload
    def __sub__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self, rhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]], rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __truediv__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __truediv__(self, rhs: float) -> VariableMatrix:
        ...
    def col(self, col: int) -> VariableBlock:
        """
        Returns a column slice of the variable matrix.
        
        Parameter ``col``:
            The column to slice.
        """
    def cols(self) -> int:
        """
        Returns number of columns in the matrix.
        """
    def cwise_transform(self, func: typing.Callable[[Variable], Variable]) -> VariableMatrix:
        """
        Transforms the matrix coefficient-wise with an unary operator.
        
        Parameter ``unary_op``:
            The unary operator to use for the transform operation.
        """
    def row(self, row: int) -> VariableBlock:
        """
        Returns a row slice of the variable matrix.
        
        Parameter ``row``:
            The row to slice.
        """
    def rows(self) -> int:
        """
        Returns number of rows in the matrix.
        """
    @typing.overload
    def set_value(self, value: float) -> None:
        """
        Assigns a double to the block.
        
        This only works for blocks with one row and one column.
        
        Parameter ``value``:
            Value to assign.
        """
    @typing.overload
    def set_value(self, values: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> None:
        """
        Sets block's internal values.
        
        Parameter ``values``:
            Eigen matrix of values.
        """
    @typing.overload
    def value(self, row: int, col: int) -> float:
        """
        Returns an element of the variable matrix.
        
        Parameter ``row``:
            The row of the element to return.
        
        Parameter ``col``:
            The column of the element to return.
        """
    @typing.overload
    def value(self, index: int) -> float:
        """
        Returns a row of the variable column vector.
        
        Parameter ``index``:
            The index of the element to return.
        """
    @typing.overload
    def value(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        """
        Returns the contents of the variable matrix.
        """
    @property
    def T(self) -> VariableMatrix:
        """
        Returns the transpose of the variable matrix.
        """
    @property
    def shape(self) -> tuple:
        ...
class VariableMatrix:
    """
    A matrix of autodiff variables.
    """
    __hash__: typing.ClassVar[None] = None
    @staticmethod
    def ones(rows: int, cols: int) -> VariableMatrix:
        """
        Returns a variable matrix filled with ones.
        
        Parameter ``rows``:
            The number of matrix rows.
        
        Parameter ``cols``:
            The number of matrix columns.
        """
    @staticmethod
    def zero(rows: int, cols: int) -> VariableMatrix:
        """
        Returns a variable matrix filled with zeroes.
        
        Parameter ``rows``:
            The number of matrix rows.
        
        Parameter ``cols``:
            The number of matrix columns.
        """
    @typing.overload
    def __add__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self: float, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self, rhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __add__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    def __array_ufunc__(self, ufunc: typing.Any, method: str, *args, **kwargs) -> typing.Any:
        ...
    @typing.overload
    def __eq__(self, rhs: VariableMatrix) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: Variable) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: int) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: Variable) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: float) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, lhs: int) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: VariableBlock) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __eq__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.EqualityConstraints:
        """
        Equality operator that returns an equality constraint for two
        Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __ge__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __getitem__(self, row: int) -> Variable:
        """
        Returns a block pointing to the given row.
        
        Parameter ``row``:
            The block row.
        """
    @typing.overload
    def __getitem__(self, slices: tuple) -> typing.Any:
        """
        Returns a block pointing to the given row and column.
        
        Parameter ``row``:
            The block row.
        
        Parameter ``col``:
            The block column.
        """
    @typing.overload
    def __gt__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __gt__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __init__(self) -> None:
        """
        Constructs an empty VariableMatrix.
        """
    @typing.overload
    def __init__(self, rows: int) -> None:
        """
        Constructs a VariableMatrix column vector with the given rows.
        
        Parameter ``rows``:
            The number of matrix rows.
        """
    @typing.overload
    def __init__(self, rows: int, cols: int) -> None:
        """
        Constructs a VariableMatrix with the given dimensions.
        
        Parameter ``rows``:
            The number of matrix rows.
        
        Parameter ``cols``:
            The number of matrix columns.
        """
    @typing.overload
    def __init__(self, list: list[list[float]]) -> None:
        """
        Constructs a scalar VariableMatrix from a nested list of doubles.
        
        This overload is for Python bindings only.
        
        Parameter ``list``:
            The nested list of Variables.
        """
    @typing.overload
    def __init__(self, list: list[list[Variable]]) -> None:
        """
        Constructs a scalar VariableMatrix from a nested list of Variables.
        
        This overload is for Python bindings only.
        
        Parameter ``list``:
            The nested list of Variables.
        """
    @typing.overload
    def __init__(self, values: Variable) -> None:
        """
        Constructs a scalar VariableMatrix from a Variable.
        
        Parameter ``variable``:
            Variable.
        """
    @typing.overload
    def __init__(self, values: VariableBlock) -> None:
        """
        Constructs a VariableMatrix from a VariableBlock.
        
        Parameter ``values``:
            VariableBlock of values.
        """
    def __iter__(self) -> typing.Iterator[Variable]:
        ...
    @typing.overload
    def __itruediv__(self, rhs: Variable) -> VariableMatrix:
        """
        Compound matrix division-assignment operator (only enabled when rhs is
        a scalar).
        
        Parameter ``rhs``:
            Variable to divide.
        """
    @typing.overload
    def __itruediv__(self, rhs: float) -> VariableMatrix:
        """
        Compound matrix division-assignment operator (only enabled when rhs is
        a scalar).
        
        Parameter ``rhs``:
            Variable to divide.
        """
    @typing.overload
    def __le__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than-or-equal-to comparison operator that returns an
        inequality constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __le__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than-or-equal-to comparison operator that returns an inequality
        constraint for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    def __len__(self) -> int:
        """
        Returns number of rows in the matrix.
        """
    @typing.overload
    def __lt__(self, rhs: VariableMatrix) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: Variable) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: float) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, lhs: int) -> _jormungandr.optimization.InequalityConstraints:
        """
        Greater-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: VariableBlock) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __lt__(self, rhs: numpy.ndarray[typing.Any, numpy.dtype[numpy.float64]]) -> _jormungandr.optimization.InequalityConstraints:
        """
        Less-than comparison operator that returns an inequality constraint
        for two Variables.
        
        Parameter ``lhs``:
            Left-hand side.
        
        Parameter ``rhs``:
            Left-hand side.
        """
    @typing.overload
    def __matmul__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __matmul__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: float) -> VariableMatrix:
        ...
    @typing.overload
    def __mul__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    def __neg__(self) -> VariableMatrix:
        ...
    def __pow__(self, power: int) -> Variable:
        ...
    @typing.overload
    def __radd__(self, lhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __radd__(self, lhs: float) -> VariableMatrix:
        ...
    @typing.overload
    def __radd__(self, lhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, lhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, lhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, lhs: float) -> VariableMatrix:
        ...
    @typing.overload
    def __rmul__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __rsub__(self, lhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __rsub__(self, lhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __setitem__(self, row: int, value: Variable) -> Variable:
        ...
    @typing.overload
    def __setitem__(self, slices: tuple, value: typing.Any) -> None:
        ...
    @typing.overload
    def __sub__(self, rhs: VariableMatrix) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self, rhs: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> VariableMatrix:
        ...
    @typing.overload
    def __sub__(self, rhs: VariableBlock) -> VariableMatrix:
        ...
    @typing.overload
    def __truediv__(self, rhs: Variable) -> VariableMatrix:
        ...
    @typing.overload
    def __truediv__(self, rhs: float) -> VariableMatrix:
        ...
    def col(self, col: int) -> VariableBlock:
        """
        Returns a column slice of the variable matrix.
        
        Parameter ``col``:
            The column to slice.
        """
    def cols(self) -> int:
        """
        Returns number of columns in the matrix.
        """
    def cwise_transform(self, func: typing.Callable[[Variable], Variable]) -> VariableMatrix:
        """
        Transforms the matrix coefficient-wise with an unary operator.
        
        Parameter ``unary_op``:
            The unary operator to use for the transform operation.
        """
    def row(self, row: int) -> VariableBlock:
        """
        Returns a row slice of the variable matrix.
        
        Parameter ``row``:
            The row to slice.
        """
    def rows(self) -> int:
        """
        Returns number of rows in the matrix.
        """
    def set_value(self, values: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]) -> None:
        """
        Sets the VariableMatrix's internal values.
        
        Parameter ``values``:
            Eigen matrix of values.
        """
    @typing.overload
    def value(self, row: int, col: int) -> float:
        """
        Returns an element of the variable matrix.
        
        Parameter ``row``:
            The row of the element to return.
        
        Parameter ``col``:
            The column of the element to return.
        """
    @typing.overload
    def value(self, index: int) -> float:
        """
        Returns a row of the variable column vector.
        
        Parameter ``index``:
            The index of the element to return.
        """
    @typing.overload
    def value(self) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]]:
        """
        Returns the contents of the variable matrix.
        """
    @property
    def T(self) -> VariableMatrix:
        """
        Returns the transpose of the variable matrix.
        """
    @property
    def shape(self) -> tuple:
        ...
@typing.overload
def abs(x: float) -> Variable:
    """
    std::abs() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def abs(x: Variable) -> Variable:
    """
    std::abs() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def acos(x: float) -> Variable:
    """
    std::acos() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def acos(x: Variable) -> Variable:
    """
    std::acos() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def asin(x: float) -> Variable:
    """
    std::asin() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def asin(x: Variable) -> Variable:
    """
    std::asin() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def atan(x: float) -> Variable:
    """
    std::atan() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def atan(x: Variable) -> Variable:
    """
    std::atan() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def atan2(y: float, x: Variable) -> Variable:
    """
    std::atan2() for Variables.
    
    Parameter ``y``:
        The y argument.
    
    Parameter ``x``:
        The x argument.
    """
@typing.overload
def atan2(y: Variable, x: float) -> Variable:
    """
    std::atan2() for Variables.
    
    Parameter ``y``:
        The y argument.
    
    Parameter ``x``:
        The x argument.
    """
@typing.overload
def atan2(y: Variable, x: Variable) -> Variable:
    """
    std::atan2() for Variables.
    
    Parameter ``y``:
        The y argument.
    
    Parameter ``x``:
        The x argument.
    """
def block(list: list[list[VariableMatrix]]) -> VariableMatrix:
    """
    Assemble a VariableMatrix from a nested list of blocks.
    
    Each row's blocks must have the same height, and the assembled block
    rows must have the same width. For example, for the block matrix [[A,
    B], [C]] to be constructible, the number of rows in A and B must
    match, and the number of columns in [A, B] and [C] must match.
    
    Parameter ``list``:
        The nested list of blocks.
    """
@typing.overload
def cos(x: float) -> Variable:
    """
    std::cos() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def cos(x: Variable) -> Variable:
    """
    std::cos() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def cosh(x: float) -> Variable:
    """
    std::cosh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def cosh(x: Variable) -> Variable:
    """
    std::cosh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def cwise_reduce(lhs: VariableMatrix, rhs: VariableMatrix, func: typing.Callable[[Variable, Variable], Variable]) -> VariableMatrix:
    """
    Applies a coefficient-wise reduce operation to two matrices.
    
    Parameter ``lhs``:
        The left-hand side of the binary operator.
    
    Parameter ``rhs``:
        The right-hand side of the binary operator.
    
    Parameter ``binary_op``:
        The binary operator to use for the reduce operation.
    """
@typing.overload
def cwise_reduce(lhs: VariableBlock, rhs: VariableBlock, func: typing.Callable[[Variable, Variable], Variable]) -> VariableMatrix:
    """
    Applies a coefficient-wise reduce operation to two matrices.
    
    Parameter ``lhs``:
        The left-hand side of the binary operator.
    
    Parameter ``rhs``:
        The right-hand side of the binary operator.
    
    Parameter ``binary_op``:
        The binary operator to use for the reduce operation.
    """
@typing.overload
def erf(x: float) -> Variable:
    """
    std::erf() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def erf(x: Variable) -> Variable:
    """
    std::erf() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def exp(x: float) -> Variable:
    """
    std::exp() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def exp(x: Variable) -> Variable:
    """
    std::exp() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def hypot(x: float, y: Variable) -> Variable:
    """
    std::hypot() for Variables.
    
    Parameter ``x``:
        The x argument.
    
    Parameter ``y``:
        The y argument.
    """
@typing.overload
def hypot(x: Variable, y: float) -> Variable:
    """
    std::hypot() for Variables.
    
    Parameter ``x``:
        The x argument.
    
    Parameter ``y``:
        The y argument.
    """
@typing.overload
def hypot(x: Variable, y: Variable) -> Variable:
    """
    std::hypot() for Variables.
    
    Parameter ``x``:
        The x argument.
    
    Parameter ``y``:
        The y argument.
    """
@typing.overload
def hypot(x: Variable, y: Variable, z: Variable) -> Variable:
    """
    std::hypot() for Variables.
    
    Parameter ``x``:
        The x argument.
    
    Parameter ``y``:
        The y argument.
    
    Parameter ``z``:
        The z argument.
    """
@typing.overload
def log(x: float) -> Variable:
    """
    std::log() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def log(x: Variable) -> Variable:
    """
    std::log() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def log10(x: float) -> Variable:
    """
    std::log10() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def log10(x: Variable) -> Variable:
    """
    std::log10() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def pow(base: float, power: Variable) -> Variable:
    """
    std::pow() for Variables.
    
    Parameter ``base``:
        The base.
    
    Parameter ``power``:
        The power.
    """
@typing.overload
def pow(base: Variable, power: float) -> Variable:
    """
    std::pow() for Variables.
    
    Parameter ``base``:
        The base.
    
    Parameter ``power``:
        The power.
    """
@typing.overload
def pow(base: Variable, power: Variable) -> Variable:
    """
    std::pow() for Variables.
    
    Parameter ``base``:
        The base.
    
    Parameter ``power``:
        The power.
    """
@typing.overload
def sign(x: float) -> Variable:
    """
    sign() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sign(x: Variable) -> Variable:
    """
    sign() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sin(x: float) -> Variable:
    """
    std::sin() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sin(x: Variable) -> Variable:
    """
    std::sin() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sinh(x: float) -> Variable:
    """
    std::sinh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sinh(x: Variable) -> Variable:
    """
    std::sinh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sqrt(x: float) -> Variable:
    """
    std::sqrt() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def sqrt(x: Variable) -> Variable:
    """
    std::sqrt() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def tan(x: float) -> Variable:
    """
    std::tan() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def tan(x: Variable) -> Variable:
    """
    std::tan() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def tanh(x: float) -> Variable:
    """
    std::tanh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
@typing.overload
def tanh(x: Variable) -> Variable:
    """
    std::tanh() for Variables.
    
    Parameter ``x``:
        The argument.
    """
