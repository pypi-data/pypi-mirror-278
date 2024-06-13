# For performance testing:
import time

#
# Base class for nodes in the computation graph
#

class Node:
    
    ## Constructor, evaluate and string representation
    def __init__(self):
        self.parents = []
    
    def Run(self):
        raise NotImplementedError("Must be implemented in subclasses")

    def __str__(self):
        raise NotImplementedError("Must be implemented in subclasses")

    ## Operator overloading to e.g. allow my.exp(x) + 3
    def __add__(self, other):
        from .NodesOperations import AddNode
        return AddNode(self, other)

    def __radd__(self, other):
        from .NodesOperations import AddNode
        return AddNode(other, self)

    def __sub__(self, other):
        from .NodesOperations import SubNode
        return SubNode(self, other)

    def __rsub__(self, other):
        from .NodesOperations import SubNode
        return SubNode(other, self)

    def __mul__(self, other):
        from .NodesOperations import MulNode
        return MulNode(self, other)

    def __rmul__(self, other):
        from .NodesOperations import MulNode
        return MulNode(other, self)

    def __truediv__(self, other):
        from .NodesOperations import DivNode
        return DivNode(self, other)

    def __rtruediv__(self, other):
        from .NodesOperations import DivNode
        return DivNode(other, self)

    def __neg__(self):
        from .NodesOperations import NegNode
        return NegNode(self)

    def __pow__(self, other):
        from .backends import BackendConfig
        pow_class = BackendConfig.backend_classes[BackendConfig.backend]["pow"]
        return pow_class(self, other)

    def __rpow__(self, other):
        from .backends import BackendConfig
        pow_class = BackendConfig.backend_classes[BackendConfig.backend]["pow"]
        return pow_class(self, other)

    def ensure_node(self, other):
        from .backends import BackendConfig
        if isinstance(other, Node):
            return other
        else:
            constant_class = BackendConfig.backend_variable_classes[BackendConfig.backend]["constant"]
            return constant_class(other)

    ## Comparison operators
    def __gt__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '>')

    def __lt__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '<')

    def __ge__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '>=')

    def __le__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '<=')

    def __eq__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '==')

    def __ne__(self, other):
        from .NodesOperations import ComparisonNode
        return ComparisonNode(self, other, '!=')
    

    ## First draft performance benchmark
    def PerformanceIteration(self):
        a = self.Run()
        b = self.grad()
        return a + b

    def run_performance_test(self, input_variables, warmup_iterations=5, test_iterations=100):
        from .backends import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)

        instance_eval_class.performance_test(input_variables[0], input_variables, warmup_iterations, test_iterations)
    
    def eval(self):
        from .backends import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class.eval()#, instance_eval_class
    
    def create_result_class(self):
        from .backends import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class
        
    def grad(self, diffDirection):
        from .backends import BackendConfig
        grad_class = BackendConfig.backend_valuation_and_grad_classes[BackendConfig.backend]["grad"]
        instance_grad_class = grad_class(self, diffDirection)
        return instance_grad_class.grad()
    
    # Additions for function creation
    def get_inputs(self):
        if self.right is not None:
          variableStrings = [self.left.get_inputs(), self.right.get_inputs()]
          return self.flatten_and_extract_unique([x for x in variableStrings if x])
        else:
          variableStrings = self.left.get_inputs()
          return self.flatten_and_extract_unique([x for x in variableStrings if x])
    
    def flatten_and_extract_unique(self, arr):  # Ensure uniqueness
        unique_strings = set()
        def traverse(sub_arr):
            for item in sub_arr:
                if isinstance(item, str):
                    unique_strings.add(item)
                elif isinstance(item, list):
                    traverse(item)
        traverse(arr)
        return list(unique_strings)
    
    def get_executable(self):
        from .NodesVariables import VariableNode

        # Get input variables
        inputs = self.get_inputs()
        def executable_func(*args):
            for input_node, arg in zip(inputs, args):
                input_node.set_value(arg)
            return self.Run()

        # Return a lambda function that calls executable_func
        return lambda *args: executable_func(*args)
    
    # Additions for function compilation
    def get_optimized_executable(self):
        from .backends import BackendConfig
        eval_class = BackendConfig.backend_result_classes[BackendConfig.backend]["result"]
        instance_eval_class = eval_class(self)
        return instance_eval_class.create_optimized_executable()

# Unary and binary node
class UnitaryNode(Node):

    def get_inputs(self):
        return self.operand.get_inputs()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class BinaryNode(Node):

    def get_inputs(self):
        inputs = [self.left.get_inputs(), self.right.get_inputs()]
        return [x for x in inputs if x]

    def get_input_variables(self):
        variableStrings = [self.left.get_input_variables(), self.right.get_input_variables()]
        return self.flatten_and_extract_unique([x for x in variableStrings if x])

# Result node for nice outputs
class ResultNode(Node):
    def __init__(self, operationNode):
        super().__init__()
        self.operationNode = operationNode



