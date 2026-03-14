from enum import Enum
from abc import ABC, abstractmethod


class Operations(Enum):
    AND = 0
    OR = 1


class Expression(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.value = None

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def prefix(self) -> str:
        pass


class Expression_bool(Expression):
    """Leaf node representing a truth value (t or f)."""
    def __init__(self, value: bool) -> None:
        self.value: bool = value

    def run(self):
        return self.value

    def prefix(self) -> str:
        return 't' if self.value else 'f'

    def __repr__(self) -> str:
        return 't' if self.value else 'f'


class Expression_logic(Expression):
    """Binary node representing a logical operation (∧ or ∨)."""
    def __init__(self, operation: Operations, left: Expression, right: Expression) -> None:
        self.operation: Operations = operation
        self.left: Expression = left
        self.right: Expression = right
        self.value = None
        assert operation in Operations

    def run(self):
        left_val = self.left.run()
        right_val = self.right.run()
        if self.operation == Operations.AND:
            self.value = left_val and right_val
        elif self.operation == Operations.OR:
            self.value = left_val or right_val
        return self.value

    def prefix(self) -> str:
        op_str = '∧' if self.operation == Operations.AND else '∨'
        return f"({op_str} {self.left.prefix()} {self.right.prefix()})"

    def __repr__(self) -> str:
        return self.prefix()


if __name__ == "__main__":
    # Test: t ∧ f = f
    b_true = Expression_bool(True)
    b_false = Expression_bool(False)
    expr = Expression_logic(Operations.AND, b_true, b_false)
    result = expr.run()
    print(f"Value: {'t' if result else 'f'}")
    print(f"Prefix: {expr.prefix()}")