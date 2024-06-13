from .Node import *

# Numerical and statistic computations
import numpy as np
import torch
import scipy
import scipy.stats
import scipy.special

# For performance testing:
import time

# Variable node
class VariableNode(UnitaryNode):
    _count = 0  # Start count from 1

    def __init__(self, value, identifier=None):
        super().__init__()
        self.value = value
        if identifier is None:
            self.identifier = f"Input{VariableNode._count}"
            VariableNode._count += 1
        else:
            self.identifier = identifier

    def set_value(self, value):
        self.value = value

    def Run(self):
        return self.value

    def __str__(self):
        return f"{self.identifier}"

    def get_inputs(self):
        return self
    
    def get_input_variables(self):
        return str(self)
    

# RandomVariable node
class RandomVariableNode(UnitaryNode):
    _countRandomVariables = 0  # Start count from 1 for RandomVariableNode instances
    def __init__(self, value=None, identifier=None):
        super().__init__()
        if identifier is None:
            identifier = f"RandomVariable{RandomVariableNode._countRandomVariables}"
            RandomVariableNode._countRandomVariables += 1
        self.identifier = identifier if identifier else f"input{VariableNode._count}"
        if value is None:
            self.value = self.NewSample()
        else:
            self.value = value
        self.sampleSize = None

    def Run(self):
        return self.value

    def __str__(self):
        return f"{self.identifier}"

    def get_inputs(self):
        return self
    
    def get_input_variables(self):
        return str(self)


# Constant node
class ConstantNode(UnitaryNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def Run(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def get_inputs(self):
      return None
    
    def get_input_variables(self):
      return ''