from .Node import *
from .NodesVariables import *
from .NodesOperations import *

# Numerical and statistic computations
import numpy as np
import scipy.stats
import scipy.special

from numba import jit

class ExpNodeNumpy(ExpNode):
    def Run(self):
        return np.exp(self.operand.Run())

    
class SinNodeNumpy(SinNode):
    def Run(self):
        return np.sin(self.operand.Run())
    
class CosNodeNumpy(SinNode):
    def Run(self):
        return np.cos(self.operand.Run())
    
class LogNodeNumpy(LogNode):
    def Run(self):
        return np.log(self.operand.Run())
    
class SqrtNodeNumpy(SqrtNode):
    def Run(self):
        return np.sqrt(self.operand.Run())
    
class PowNodeNumpy(PowNode):
    def Run(self):
        return self.left.Run() ** self.right.Run()
    
class CdfNodeNumpy(CdfNode):
    def Run(self):
        return scipy.stats.norm.cdf(self.operand.Run())
    
class ErfNodeNumpy(ErfNode):
    def Run(self):
        return scipy.special.erf(self.operand.Run())

class ErfinvNodeNumpy(ErfinvNode):
    def Run(self):
        return scipy.special.erfinv(self.operand.Run())

class MaxNodeNumpy(MaxNode):
    def Run(self):
        return np.maximum(self.left.Run(), self.right.Run())

class RandomVariableNodeNumpy(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.value = np.random.uniform(size = sampleSize)

class RandomVariableNodeNumpyNormal(RandomVariableNode):
    def NewSample(self, sampleSize = 1):
        self.value = np.random.normal(size = sampleSize)

class SumNodeVectorizedNumpy(Node):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"sumVectorized({str(self.operand)})"

    def Run(self):
        return np.sum(self.operand.Run())
    
    # We use sum of an array only, hence here we don't have to iterate through an array.
    def get_inputs(self):
        return self.operand.get_inputs()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class IfNodeNumpy(IfNode):
        def Run(self):
            condition_value = self.condition.Run()
            true_value = self.true_value.Run()
            false_value = self.false_value.Run()
            return np.where(condition_value, true_value, false_value)

class GradNodeNumpy(GradNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def grad(self):
        result = self.Run()
        h = 0.00001
        self.diffDirection.value = self.diffDirection.value + h
        result_h = self.Run()
        return (result_h - result) / h
    
class ResultNodeNumpy(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)

    def eval(self):
        return self.operationNode.Run()
    
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


        for _ in range(warmup_iterations):
            result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            derivative_optimized = self.grad_of_function(myfunc, args_dict)

        for _ in range(test_iterations):
            tic = time.time()

            result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            derivative_optimized = self.grad_of_function(myfunc, args_dict)

            toc = time.time()
            spent = toc - tic
            times_optimized.append(spent)
            time_total_optimized += spent

            results_optimized.append(result_optimized)
            deltas_optimized.append(derivative_optimized)
            
        # Compute runtimes
        # mean_time_standard =  total_time / test_iterations
        # variance_time_standard =  sum((time - mean_time_standard) ** 2 for time in times) / (test_iterations - 1)    
        mean_time_optimized = time_total_optimized / test_iterations
        variance_time_optimized = sum((time - mean_time_optimized) ** 2 for time in times_optimized) / (test_iterations - 1)

        # Output results in table format
        print("{:<20} {:<12} {:<20} {:<15} {:<16}".format('Backend', 'Result', 'Gradient (1. entry)', 'mean runtime', 'variance runtime'))
        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("nump", sum(results_standard) / test_iterations, sum(deltas_standard) / test_iterations, mean_time_standard, variance_time_standard))
        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("numpy_jit", sum(results_optimized) / test_iterations, sum(deltas_optimized) / test_iterations, mean_time_optimized, variance_time_optimized))
   
    def grad_of_function(sef, func, args_dict, h = 0.00001):
        result = func(**args_dict)
        args_dict_shifted = args_dict.copy()
        args_dict_shifted['s0'] += h
        result_h = func(**args_dict_shifted)
        return (result_h - result) / h
    
    def create_optimized_executable(self):
        def create_function_from_expression(expression_string, expression_inputs, backend):
            # Generate the function definition as a string
            inputs = ", ".join(expression_inputs)
            function_code = f"def myfunc({inputs}):\n    return {expression_string}\n"
            
            # Print the generated function code
            #print("Generated Function Code for numpy:")
            #print(function_code)

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
            "constant" : "",
            "exp": "np.exp",
            "sin": "np.sin",
            "cos": "np.cos",
            "pow": "np.pow",
            "log": "np.log",
            "sqrt": "np.sqrt",
            "cdf": "np.cdf",
            "erf": "scipy.special.erf",
            "erfinv": "scipy.special.erfinv",
            "max": "np.max",
            "sumVectorized": "np.sum",
            "seed": "np.seed",
            "if": "np.where"
        }
        
        for key, value in function_mappings.items():
            expression = expression.replace(key, value)

        input_names = self.operationNode.get_input_variables()

        numpy_func = create_function_from_expression(expression, input_names,  {'np': np, 'scipy.special' : scipy.special})
        jitted_numpy_func = jit(nopython=True)(numpy_func)

        return  jitted_numpy_func# numpy_func
