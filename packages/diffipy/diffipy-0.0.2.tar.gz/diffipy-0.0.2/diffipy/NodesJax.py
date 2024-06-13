from .Node import *
from .NodesVariables import *
from .NodesOperations import *

import jax
import jax.numpy as jnp

class VariableNodeJAX(VariableNode):
    def __init__(self, value, identifier=None):
        super().__init__(value, identifier)
        self.value = jnp.array(self.value)

    def Run(self):
        return self.value
    
class RandomVariableNodeJAX(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        z_jax = jax.random.normal(jax.random.PRNGKey(0), shape=(1, sampleSize))
        self.value = 0.5 * (1 + jax.scipy.special.erf(z_jax / jnp.sqrt(2.0)))

class RandomVariableNodeJAXNormal(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        self.value = jax.random.normal(jax.random.PRNGKey(0), shape=(1, sampleSize))

class ConstantNodeJAX(ConstantNode):
    def Run(self):
        return jnp.array(self.value)
    def __str__(self):
        return f"constant({str(self.value)})"

class ExpNodeJAX(ExpNode):
    def Run(self):
        return jnp.exp(self.operand.Run())
    
class SinNodeJAX(SinNode):
    def Run(self):
        return jnp.sin(self.operand.Run())
    
class CosNodeJAX(CosNode):
    def Run(self):
        return jnp.cos(self.operand.Run())

class LogNodeJAX(LogNode):
    def Run(self):
        return jnp.log(self.operand.Run())

class SqrtNodeJAX(SqrtNode):
    def Run(self):
        return jnp.sqrt(self.operand.Run())

class PowNodeJAX(PowNode):
    def Run(self):
        return jnp.power(self.left.Run(), self.right.Run())

class CdfNodeJAX(CdfNode):
    def Run(self):
        return 0.5 * (jax.scipy.special.erf(self.operand.Run() / jnp.sqrt(2.0)) + 1.0)

class ErfNodeJAX(ErfNode):
    def Run(self):
        return jax.scipy.special.erf(self.operand.Run())

class ErfinvNodeJAX(ErfinvNode):
    def Run(self):
        return jax.scipy.special.erfinv(self.operand.Run())

class MaxNodeJAX(MaxNode):
    def Run(self):
        return jnp.maximum(self.left.Run(), self.right.Run())

class SumNodeVectorizedJAX(Node):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"sumVectorized({str(self.operand)})"

    def Run(self):
        return jnp.sum(self.operand.Run())
    
        # We use sum of tensors only, hence here we don't have to iterate through an array.
    def get_inputs(self):
        return self.operand.get_inputs()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class IfNodeJAX(IfNode):
    def __init__(self, condition, true_value, false_value):
        super().__init__(condition, true_value, false_value)

    def Run(self):
        condition_value = self.condition.Run()
        true_value = self.true_value.Run()
        false_value = self.false_value.Run()
        return jnp.where(condition_value, true_value, false_value)

class GradNodeJAX(GradNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def grad(self):
        inputs = self.get_inputs()
        executable = self.get_executable()
        grad_my_function = jax.grad(executable)(inputs[0].value)
        
        return grad_my_function
    

class ResultNodeJAX(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)

    def eval(self):
        return self.operationNode.Run().item()
    
    def performance_test(self, diffDirection, input_variables, warmup_iterations, test_iterations):
        #return
        total_time = 0.0
        results_standard = []
        deltas_standard = []
        times = []

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
            def myfunc_with_dict(args_dict):
                return myfunc(**args_dict)
            gradient_func = jax.grad(myfunc_with_dict)

        for _ in range(test_iterations):
            tic = time.time()

            result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            def myfunc_with_dict(args_dict):
                return myfunc(**args_dict)
            
            gradient_func = jax.grad(myfunc_with_dict)
            derivative_optimized = gradient_func(args_dict)


            toc = time.time()
            spent = toc - tic
            times_optimized.append(spent)
            time_total_optimized += spent

            results_optimized.append(result_optimized)
            deltas_optimized.append(derivative_optimized)
            
        # Compute runtimes
        mean_time_optimized = time_total_optimized / test_iterations
        variance_time_optimized = sum((time - mean_time_optimized) ** 2 for time in times_optimized) / (test_iterations - 1)

        # Output results in table format
        s0_grads = [result['s0'] for result in deltas_optimized]
        s0_mean = jnp.mean(jnp.array(s0_grads))

        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("jax", sum(results_optimized) / test_iterations, s0_mean, mean_time_optimized, variance_time_optimized))
   
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
            
            # Compile the function code
            compiled_code = compile(function_code, "<string>", "exec")
            
            # Combine the provided backend with an empty dictionary to serve as the globals
            namespace = {**backend}
            exec(compiled_code, namespace)
            return namespace["myfunc"]

        expression = str(self.operationNode)

        # Replace function names in the expression string
        function_mappings = {
            "constant" : "",
            "exp": "jnp.exp",
            "sin": "jnp.sin",
            "cos": "jnp.cos",
            "pow": "jnp.pow",
            "log": "jnp.log",
            "sqrt": "jnp.sqrt",
            "cdf": "jnp.cdf",
            "erf": "jax.scipy.special.erf",
            "erfinv": "jax.scipy.special.erfinv",
            "max": "jnp.max",
            "sumVectorized": "jnp.sum",
            "seed": "jnp.seed",
            "if": "jnp.where"
        }
        
        for key, value in function_mappings.items():
            expression = expression.replace(key, value)

        input_names = self.operationNode.get_input_variables()

        numpy_func = create_function_from_expression(expression, input_names,  {'jax': jax, 'jnp' : jax.numpy})
        #jitted_numpy_func = jit(nopython=True)(numpy_func)
        jax.make_jaxpr(numpy_func)
        return  numpy_func#jitted_numpy_func# numpy_func

