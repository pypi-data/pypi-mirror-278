from .Node import *


# Addition node
class AddNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def Run(self):
        return self.left.Run() + self.right.Run()

    def __str__(self):
        return f"({str(self.left)} + {str(self.right)})"

# Subtraction node
class SubNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def Run(self):
        return self.left.Run() - self.right.Run()

    def __str__(self):
        return f"({str(self.left)} - {str(self.right)})"

# Multiplication node
class MulNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def Run(self):
        return self.left.Run() * self.right.Run()

    def __str__(self):
        return f"({str(self.left)} * {str(self.right)})"

# Division node
class DivNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def Run(self):
        return self.left.Run() / self.right.Run()

    def __str__(self):
        return f"({str(self.left)} / {str(self.right)})"

# Negation node
class NegNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def Run(self):
        return -self.operand.Run()

    def __str__(self):
        return f"(-{str(self.operand)})"

# Exponential function node
class ExpNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"exp({str(self.operand)})"

# Sin function node
class SinNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"sin({str(self.operand)})"
    
# Cos function node
class CosNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"cos({str(self.operand)})"


# Logarithm function node
class LogNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"log({str(self.operand)})"





# Square root function node
class SqrtNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"sqrt({str(self.operand)})"




# Power function node
class PowNode(BinaryNode):
    def __init__(self, left, right): # left = base, right = exponent
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def __str__(self):
        return f"({str(self.left)} ** {str(self.right)})"




# Standard normal cdf
class CdfNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"cdf({str(self.operand)})"


# Error function node
class ErfNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"erf({str(self.operand)})"



# Inverse error function node
class ErfinvNode(UnitaryNode):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"erfinv({str(self.operand)})"


# Maximum node
class MaxNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.parents = [self.left, self.right]

    def __str__(self):
        return f"max({str(self.left)}, {str(self.right)})"

# Summation node
class SumNode(Node):
    def __init__(self, operands):
        super().__init__()
        self.operands = [self.ensure_node(op) for op in operands]
        self.parents = self.operands

    def Run(self):
        return sum(op.Run() for op in self.operands)

    def __str__(self):
        operands_str = ', '.join(str(op) for op in self.operands)
        return f"sum({operands_str})"

    def get_inputs(self):
        inputs = [var for op in self.operands for var in op.get_inputs()]
        return self.flatten_and_extract_unique([x for x in inputs if x])
    
    def get_input_variables(self):
        variableStrings = [var for op in self.operands for var in op.get_input_variables()]
        return self.flatten_and_extract_unique([x for x in variableStrings if x])


    


# Conditional (if) node
class IfNode(Node):
    def __init__(self, condition, true_value, false_value):
        super().__init__()
        self.condition = self.ensure_node(condition)
        self.true_value = self.ensure_node(true_value)
        self.false_value = self.ensure_node(false_value)
        self.parents = [self.condition, self.true_value, self.false_value]
        self.payoff_bfs = None

    def __str__(self):
        return f"if({str(self.condition)}, {str(self.true_value)}, {str(self.false_value)})"

    def ConditionToString(self):
        return f"{str(self.condition)}"

    def get_inputs(self):
        inputs = [self.condition.get_inputs(), self.true_value.get_inputs(), self.false_value.get_inputs()]
        return self.flatten_and_extract_unique([x for x in inputs if x])
    
    
    def get_input_variables(self):
        variableStrings = [self.condition.get_input_variables(), self.true_value.get_input_variables(), self.false_value.get_input_variables()]
        return self.flatten_and_extract_unique([x for x in variableStrings if x])


# Comparison node
class ComparisonNode(Node):
    def __init__(self, left, right, op):
        super().__init__()
        self.left = self.ensure_node(left)
        self.right = self.ensure_node(right)
        self.op = op
        self.parents = [self.left, self.right]

    def Run(self):
        if self.op == '>':
            return self.left.Run() > self.right.Run()
        elif self.op == '<':
            return self.left.Run() < self.right.Run()
        elif self.op == '==':
            return self.left.Run() == self.right.Run()
        elif self.op == '!=':
            return self.left.Run() != self.right.Run()
        elif self.op == '>=':
            return self.left.Run() >= self.right.Run()
        elif self.op == '<=':
            return self.left.Run() <= self.right.Run()
        else:
            raise ValueError(f"Unsupported comparison operator: {self.op}")

    def __str__(self):
        return f"({str(self.left)} {self.op} {str(self.right)})"

    def get_inputs(self):
        inputs = [self.left.get_inputs(), self.right.get_inputs()]
        return self.flatten_and_extract_unique([x for x in inputs if x])
    
    
    def get_input_variables(self):
        variableStrings = [self.left.get_input_variables(), self.right.get_input_variables()]
        return self.flatten_and_extract_unique([x for x in variableStrings if x])
    
# Logarithm function node
class GradNode(UnitaryNode):
    def __init__(self, operand, diffDirection):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]
        self.diffDirection = diffDirection

    def Run(self):
        return self.operand.Run()

    def __str__(self):
        return f"grad({str(self.operand)})"


