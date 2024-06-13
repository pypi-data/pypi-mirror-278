from .NodesPytorch import *
from .NodesNumpy import *
from .NodesTensorflow import *
from .NodesJax import *

class BackendConfig:
    backend = 'numpy'  # default

# Add the necessary classes to backend_classes
    backend_classes = {
        "torch": {"exp": ExpNodeTorch, "pow": PowNodeTorch, "log": LogNodeTorch,
                "sqrt": SqrtNodeTorch, "cdf": CdfNodeTorch, "erf": ErfNodeTorch,
                "erfinv": ErfinvNodeTorch, "max": MaxNodeTorch, "sumVectorized": SumNodeVectorizedTorch,
                "seed": lambda value: torch.manual_seed(value),
                "if": IfNodeTorch, "sin": SinNodeTorch, "cos": CosNodeTorch},
        "numpy": {"exp": ExpNodeNumpy, "pow": PowNodeNumpy, "log": LogNodeNumpy,
                "sqrt": SqrtNodeNumpy, "cdf": CdfNodeNumpy, "erf": ErfNodeNumpy,
                "erfinv": ErfinvNodeNumpy, "max": MaxNodeNumpy, "sumVectorized": SumNodeVectorizedNumpy,
                "seed": lambda value: np.random.seed(seed=value), "if": IfNodeNumpy, "sin": SinNodeNumpy, "cos": CosNodeNumpy},
        "tensorflow": {"exp": ExpNodeTF, "pow": PowNodeTF, "log": LogNodeTF,
                "sqrt": SqrtNodeTF, "cdf": CdfNodeTF, "erf": ErfNodeTF,
                "erfinv": ErfinvNodeTF, "max": MaxNodeTF, "sumVectorized": SumNodeVectorizedTF,
                "seed": lambda value: tf.random.set_seed(value), "if": IfNodeTF, "sin": SinNodeTF, "cos": CosNodeTF},
        "jax": {"exp": ExpNodeJAX, "pow": PowNodeJAX, "log": LogNodeJAX,
                "sqrt": SqrtNodeJAX, "cdf": CdfNodeJAX, "erf": ErfNodeJAX,
                "erfinv": ErfinvNodeJAX, "max": MaxNodeJAX, "sumVectorized": SumNodeVectorizedJAX,
                "seed": lambda value: jax.random.PRNGKey(seed=value), "if": IfNodeJAX, "sin": SinNodeJAX, "cos": CosNodeJAX}
    }



    backend_variable_classes = {
        "torch": {"randomVariable": RandomVariableNodeTorch, "constant": ConstantNodeTorch, "input": VariableNodeTorch, "randomVariableNormal": RandomVariableNodeTorchNormal},
        "numpy": {"randomVariable": RandomVariableNodeNumpy, "constant": ConstantNode, "input": VariableNode, "randomVariableNormal": RandomVariableNodeNumpyNormal},
        "tensorflow": {"randomVariable": RandomVariableNodeTF, "constant": ConstantNodeTF, "input": VariableNodeTF, "randomVariableNormal": RandomVariableNodeTFNormal},
        "jax": {"randomVariable": RandomVariableNodeJAX, "constant": ConstantNodeJAX, "input": VariableNodeJAX, "randomVariableNormal": RandomVariableNodeJAXNormal}
    }

    backend_valuation_and_grad_classes = {
        "torch": {"grad": GradNodeTorch},
        "numpy": {"grad": GradNodeNumpy},
        "tensorflow": {"grad": GradNodeTF},
        "jax": {"grad": GradNodeJAX}
    }

    backend_result_classes = {
        "torch": {"result": ResultNodeTorch},
        "numpy": {"result": ResultNodeNumpy},
        "tensorflow": {"result": ResultNodeTF},
        "jax": {"result": ResultNodeJAX}
    }
