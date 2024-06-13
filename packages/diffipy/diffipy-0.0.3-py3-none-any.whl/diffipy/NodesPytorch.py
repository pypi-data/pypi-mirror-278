from .Node import *
from .NodesVariables import *
from .NodesOperations import *

# Numerical and statistic computations
import torch

# Subclass for PyTorch
class VariableNodeTorch(VariableNode):
    def __init__(self, value, identifier=None):
        super().__init__(value, identifier)
        self.torch_tensor = torch.tensor(self.value, requires_grad=True)
        self.require_grad = True
        self.value = self.torch_tensor

    def Run(self):
        return self.torch_tensor
    

# Subclass for PyTorch
class RandomVariableNodeTorch(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.SampleSize = sampleSize
        z_torch = torch.normal(mean=0, std=1, size=(1,sampleSize))
        self.value = 0.5 * (1 + torch.erf(z_torch / torch.sqrt(torch.tensor(2.0))))

# Subclass for PyTorch
class RandomVariableNodeTorchNormal(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.SampleSize = sampleSize
        self.value = torch.normal(mean=0, std=1, size=(1,sampleSize))



# Subclass for PyTorch
class ConstantNodeTorch(ConstantNode):
    def Run(self):
        return torch.tensor(self.value)
    
    def __str__(self):
        return f"constant({str(self.value)})"

    
# Subclass for PyTorch
class SinNodeTorch(SinNode):
    def Run(self):
        return torch.sin(self.operand.Run())
    
# Subclass for PyTorch
class CosNodeTorch(CosNode):
    def Run(self):
        return torch.cos(self.operand.Run())

# Subclass for PyTorch
class ExpNodeTorch(ExpNode):
    def Run(self):
        return torch.exp(self.operand.Run())



# Subclass for PyTorch
class LogNodeTorch(LogNode):
    def Run(self):
        return torch.log(self.operand.Run())
    

# Subclass for PyTorch
class SqrtNodeTorch(SqrtNode):
    def Run(self):
        return torch.sqrt(self.operand.Run())



# Subclass for PyTorch
class PowNodeTorch(PowNode):
    def Run(self):
        return torch.pow(self.left.Run(), self.right.Run())



# Subclass for PyTorch
class CdfNodeTorch(CdfNode):
    def Run(self):
        return 0.5 * (torch.erf(self.operand.Run() / torch.sqrt(torch.tensor(2.0))) + 1.0 )



# Subclass for PyTorch
class ErfNodeTorch(ErfNode):
    def Run(self):
        return torch.erf(self.operand.Run())
    

# Subclass for PyTorch
class ErfinvNodeTorch(ErfinvNode):
    def Run(self):
        return torch.erfinv(self.operand.Run())
    

# Subclass for PyTorch
class MaxNodeTorch(MaxNode):
    def Run(self):
        return torch.maximum(self.left.Run(), self.right.Run())
    



class SumNodeVectorizedTorch(Node):
    def __init__(self, operands):
        super().__init__()
        self.operands = self.ensure_node(operands)
        self.parents = [self.operands]

    def __str__(self):
        return f"sumVectorized({str(self.operands)})"

    def Run(self):
        return torch.sum(self.operands.Run())
    
    # We use sum of tensors only, hence here we don't have to iterate through an array.
    def get_inputs(self):
        return self.operands.get_inputs()
    def get_input_variables(self):
        return self.operands.get_input_variables()

    # def get_inputs(self):
    #     inputs = [var for op in self.operands for var in op.get_inputs()]
    #     return self.flatten_and_extract_unique([x for x in inputs if x])
    
    # def get_input_variables(self):
    #     print(self.operands)
    #     variableStrings = [var for op in self.operands for var in op.get_input_variables()]
    #     return self.flatten_and_extract_unique([x for x in variableStrings if x])



class IfNodeTorch(IfNode):
    def __init__(self, condition, true_value, false_value):
      super().__init__(condition, true_value, false_value)

    def Run(self):
      condition_value = self.condition.Run()
      true_value = self.true_value.Run()
      false_value = self.false_value.Run()
      return torch.where(condition_value, true_value, false_value)
    

# Subclass for PyTorch
class GradNodeTorch(GradNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def grad(self):
        # Reset derivative graph
        self.diffDirection.torch_tensor.grad = None
        forwardevaluation = self.Run()

        # Backward
        forwardevaluation.backward()

        # Return S0 derivative
        derivative = self.diffDirection.torch_tensor.grad.item()
        return derivative
    
class ResultNodeTorch(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)

    def eval(self):
        return self.operationNode.Run().item()
        
    def performance_test(self, diffDirection, input_variables, warmup_iterations, test_iterations):
        total_time = 0.0
        results_standard = []
        deltas_standard = []
        times = []

        for _ in range(warmup_iterations):
            result_standard = self.operationNode.eval()
            delta_standard = self.operationNode.grad(diffDirection)

        for _ in range(test_iterations):
            tic = time.time()

            #z.value = pre_computed_random_variables
            result_standard = self.operationNode.eval()
            delta_standard = self.operationNode.grad(diffDirection)

            toc = time.time()
            spent = toc - tic
            times.append(spent)
            total_time += spent
            results_standard.append(result_standard)
            deltas_standard.append(delta_standard)

        # Compute runtimes
        mean_time_standard =  total_time / test_iterations
        variance_time_standard =  sum((time - mean_time_standard) ** 2 for time in times) / (test_iterations - 1)    


        values = [var.value for var in input_variables]
        args_dict = {var.identifier: var.value for var in input_variables}

        ###
        ### Test performance of optimized executable
        ###

        myfunc = self.operationNode.get_optimized_executable()

        #di.seed(seed)
        time_total_optimized = 0
        times_optimized = []
        results_optimized = []
        deltas_optimized = []

        #pre_computed_random_variables = z.value #torch.normal(mean=0, std=1, size=(1, N))

        for _ in range(warmup_iterations):
            result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            diffDirection.torch_tensor.grad = None
            result_optimized.backward()
            derivative_optimized = diffDirection.torch_tensor.grad.item()

        for _ in range(test_iterations):
            tic = time.time()

            result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            diffDirection.torch_tensor.grad = None
            result_optimized.backward()
            derivative_optimized = diffDirection.torch_tensor.grad.item()

            toc = time.time()
            spent = toc - tic
            times_optimized.append(spent)
            time_total_optimized += spent

            results_optimized.append(result_optimized.item())
            deltas_optimized.append(derivative_optimized)
            
        # Compute runtimes
        # mean_time_standard =  total_time / test_iterations
        # variance_time_standard =  sum((time - mean_time_standard) ** 2 for time in times) / (test_iterations - 1)    
        mean_time_optimized = time_total_optimized / test_iterations
        variance_time_optimized = sum((time - mean_time_optimized) ** 2 for time in times_optimized) / (test_iterations - 1)

        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("torch", sum(results_standard) / test_iterations, sum(deltas_standard) / test_iterations, mean_time_standard, variance_time_standard))
        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("torch_optimized", sum(results_optimized) / test_iterations, sum(deltas_optimized) / test_iterations, mean_time_optimized, variance_time_optimized))

    def create_optimized_executable(self):
            def create_function_from_expression(expression_string, expression_inputs, backend):
                # Generate the function definition as a string
                inputs = ", ".join(expression_inputs)
                function_code = f"def myfunc({inputs}):\n    return {expression_string}\n"
                
                # Print the generated function code
                # print("Generated Function Code:")
                # print(function_code)

                # Compile the function code
                compiled_code = compile(function_code, "<string>", "exec")
                
                # Combine the provided backend with an empty dictionary to serve as the globals
                namespace = {**backend}
                exec(compiled_code, namespace)
                
                # Retrieve the dynamically created function
                #created_function = namespace["myfunc"]
            
                # Return the dynamically created function
                return namespace["myfunc"]

            expression = str(self.operationNode)

                # Replace function names in the expression string
            function_mappings = {
                "constant" : "torch.tensor",
                "exp": "torch.exp",
                "sin": "torch.sin",
                "cos": "torch.cos",
                "pow": "torch.pow",
                "log": "torch.log",
                "sqrt": "torch.sqrt",
                "cdf": "torch.cdf",
                "erf": "torch.erf",
                "erfinv": "torch.erfinv",
                "max": "torch.max",
                "sumVectorized": "torch.sum",
                "seed": "torch.seed",
                "if": "torch.where"
            }
            
            for key, value in function_mappings.items():
                expression = expression.replace(key, value)

            #expression = expression.replace('exp', 'torch.exp').replace('sqrt', 'torch.sqrt').replace('log', 'torch.log').replace('sin', 'torch.sin')
            input_names = self.operationNode.get_input_variables()

            torch_func = create_function_from_expression(expression, input_names,  {'torch': torch})

            # Wrap it such that it can get values as inputs
            def myfunc_wrapper(func):
                def wrapped_func(*args):#, **kwargs):
                    # Convert all positional arguments to torch.tensor
                    converted_args = [torch.tensor(arg.value) for arg in args]
                    
                    # # Convert all keyword arguments to torch.tensor
                    # converted_kwargs = {key: torch.tensor(value) for key, value in kwargs.items()}
                    
                    # Call the original function with converted arguments
                    return func(*converted_args)#, **converted_kwargs)
                
                return wrapped_func

            return torch_func#myfunc_wrapper(torch_func) #returning it in such a way that it needs tensor inputs for now