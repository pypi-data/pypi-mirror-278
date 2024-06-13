from .Node import *
from .NodesVariables import *
from .NodesOperations import *

import tensorflow as tf

class VariableNodeTF(VariableNode):
    def __init__(self, value, identifier=None):
        super().__init__(value, identifier)
        self.value = tf.Variable(self.value, dtype=tf.float32)

    def Run(self):
        return self.value

class RandomVariableNodeTF(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        z_tf = tf.random.normal(shape=(1, sampleSize))
        self.value = 0.5 * (1 + tf.math.erf(z_tf / tf.sqrt(2.0)))

class RandomVariableNodeTFNormal(RandomVariableNode):
    def NewSample(self, sampleSize=1):
        self.SampleSize = sampleSize
        self.value = tf.random.normal(shape=(1, sampleSize))

class ConstantNodeTF(ConstantNode):
    def Run(self):
        return tf.constant(self.value, dtype=tf.float32)
    def __str__(self):
        return f"constant({str(self.value)})"

class ExpNodeTF(ExpNode):
    def Run(self):
        return tf.exp(self.operand.Run())
    
class LogNodeTF(LogNode):
    def Run(self):
        return tf.log(self.operand.Run())
    
class SinNodeTF(SinNode):
    def Run(self):
        return tf.sin(self.operand.Run())

class CosNodeTF(CosNode):
    def Run(self):
        return tf.cos(self.operand.Run())

class SqrtNodeTF(SqrtNode):
    def Run(self):
        return tf.sqrt(self.operand.Run())

class PowNodeTF(PowNode):
    def Run(self):
        return tf.pow(self.left.Run(), self.right.Run())

class CdfNodeTF(CdfNode):
    def Run(self):
        return 0.5 * (tf.math.erf(self.operand.Run() / tf.sqrt(2.0)) + 1.0)

class ErfNodeTF(ErfNode):
    def Run(self):
        return tf.math.erf(self.operand.Run())

class ErfinvNodeTF(ErfinvNode):
    def Run(self):
        return tf.math.erfinv(self.operand.Run())

class MaxNodeTF(MaxNode):
    def Run(self):
        return tf.maximum(self.left.Run(), self.right.Run())

class SumNodeVectorizedTF(Node):
    def __init__(self, operand):
        super().__init__()
        self.operand = self.ensure_node(operand)
        self.parents = [self.operand]

    def __str__(self):
        return f"sumVectorized({str(self.operand)})"

    def Run(self):
        return tf.reduce_sum(self.operand.Run())
        
    # We use sum of tensors only, hence here we don't have to iterate through an array.
    def get_inputs(self):
        return self.operand.get_inputs()
    def get_input_variables(self):
        return self.operand.get_input_variables()

class IfNodeTF(IfNode):
    def __init__(self, condition, true_value, false_value):
        super().__init__(condition, true_value, false_value)

    def Run(self):
        condition_value = self.condition.Run()
        true_value = self.true_value.Run()
        false_value = self.false_value.Run()
        return tf.where(condition_value, true_value, false_value)

class GradNodeTF(GradNode):
    def __init__(self, operand, diffDirection):
        super().__init__(operand, diffDirection)

    def grad(self):
        with tf.GradientTape() as tape:
            forward_evaluation = self.Run()
        return tape.gradient(forward_evaluation, self.diffDirection.value).numpy()

class ResultNodeTF(ResultNode):
    def __init__(self, operationNode):
        super().__init__(operationNode)

    def eval(self):
        return self.operationNode.Run().numpy().item()
    
    def performance_test(self, diffDirection, input_variables, warmup_iterations, test_iterations):
        total_time = 0.0
        results_standard = []
        deltas_standard = []
        times = []

        for _ in range(warmup_iterations):
            result_standard = self.operationNode.eval()
            delta_standard = self.operationNode.grad(diffDirection)

        #print(delta_standard)
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

        #pre_computed_random_variables = z.value #tf.normal(mean=0, std=1, size=(1, N))

        for _ in range(warmup_iterations):
            with tf.GradientTape() as tape:
                result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            derivative_optimized = tape.gradient(result_optimized, diffDirection.value)
            # diffDirection.tensorflow_tensor.grad = None
            # result_optimized.backward()
            # derivative_optimized = diffDirection.tensorflow_tensor.grad.item()

        for _ in range(test_iterations):
            tic = time.time()

            with tf.GradientTape() as tape:
                result_optimized = myfunc(**args_dict)#s0=s0.value, K=K.value, r=r.value, sigma=sigma.value, dt = dt.value, z=pre_computed_random_variables)
            derivative_optimized = tape.gradient(result_optimized, diffDirection.value)
            
            toc = time.time()
            spent = toc - tic
            times_optimized.append(spent)
            time_total_optimized += spent

            results_optimized.append(np.sum(result_optimized.numpy()))
            deltas_optimized.append(derivative_optimized.numpy())
            
        # Compute runtimes
        # mean_time_standard =  total_time / test_iterations
        # variance_time_standard =  sum((time - mean_time_standard) ** 2 for time in times) / (test_iterations - 1)    
        mean_time_optimized = time_total_optimized / test_iterations
        variance_time_optimized = sum((time - mean_time_optimized) ** 2 for time in times_optimized) / (test_iterations - 1)

        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("tensorflow", sum(results_standard) / test_iterations, sum(deltas_standard) / test_iterations, mean_time_standard, variance_time_standard))
        print("{:<20} {:<12.6f} {:<20.6f} {:<15.6f} {:<15.6f}".format("tensorflow_optimized", sum(results_optimized) / test_iterations, sum(deltas_optimized) / test_iterations, mean_time_optimized, variance_time_optimized))

    def create_optimized_executable(self):
            def create_function_from_expression(expression_string, expression_inputs, backend):
                # Generate the function definition as a string
                inputs = ", ".join(expression_inputs)
                function_code = f"def myfunc({inputs}):\n    return {expression_string}\n"
                
                # Print the generated function code
                #print("Generated Function Code:")
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
                #"constant" : "tf.Variable",
                "exp": "tf.exp",
                "sin": "tf.sin",
                "cos": "tf.cos",
                "pow": "tf.pow",
                "log": "tf.log",
                "sqrt": "tf.sqrt",
                "cdf": "tf.cdf",
                "erf": "tf.erf",
                "erfinv": "tf.erfinv",
                "max": "tf.max",
                "sumVectorized": "tf.math.reduce_sum",
                "seed": "tf.seed",
                "if": "tf.where"
            }

            import re
            
            for key, value in function_mappings.items():
                expression = expression.replace(key, value)

            # Function to replace 'constant' with 'tf.Variable'
            def replace_constant(match):
                value = match.group(1)
                # return f"tf.Variable({value}, dtype=tf.float32)"
                return f"tf.Variable({value}, dtype=tf.float32)"
            expression = re.sub(r'constant\(([^)]+)\)', replace_constant, expression)

            #expression = expression.replace('exp', 'tf.exp').replace('sqrt', 'tf.sqrt').replace('log', 'tf.log').replace('sin', 'tf.sin')
            input_names = self.operationNode.get_input_variables()

            tensorflow_func = create_function_from_expression(expression, input_names,  {'tf': tf})

            return tensorflow_func#myfunc_wrapper(tensorflow_func) #returning it in such a way that it needs tensor inputs for now
