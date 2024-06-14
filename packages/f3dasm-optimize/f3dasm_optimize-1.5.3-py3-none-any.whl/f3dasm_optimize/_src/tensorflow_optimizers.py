"""
Information on the Adam optimizer
"""
#                                                                       Modules
# =============================================================================


# Standard
from typing import List

# Third-party
import tensorflow as tf

from ._protocol import Domain
# Locals
from .adapters.tensorflow_implementations import TensorflowOptimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class AdamTensorflow(TensorflowOptimizer):
    """Adam"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 beta_1: float = 0.9, beta_2: float = 0.999,
                 epsilon: float = 1e-07, amsgrad: bool = False, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.amsgrad = amsgrad
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Adam(
            learning_rate=self.learning_rate,
            beta_1=self.beta_1,
            beta_2=self.beta_2,
            epsilon=self.epsilon,
            amsgrad=self.amsgrad,
        )

    def _get_info(self) -> List[str]:
        return ['Stable', 'Global', 'First-Order', 'Single-Solution']

# =============================================================================


class Adamax(TensorflowOptimizer):
    """Adamax"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 beta_1: float = 0.9, beta_2: float = 0.999,
                 epsilon: float = 1e-07, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Adamax(
            learning_rate=self.learning_rate,
            beta_1=self.beta_1,
            beta_2=self.beta_2,
            epsilon=self.epsilon,
        )

    def _get_info(self) -> List[str]:
        return ['Fast', 'Single-Solution']

# =============================================================================


class Ftrl(TensorflowOptimizer):
    """Ftrl"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 learning_rate_power: float = -0.5,
                 initial_accumulator_value: float = 0.1,
                 l1_regularization_strength: float = 0.0,
                 l2_regularization_strength: float = 0.0,
                 l2_shrinkage_regularization_strength: float = 0.0,
                 beta: float = 0.0, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.learning_rate_power = learning_rate_power
        self.initial_accumulator_value = initial_accumulator_value
        self.l1_regularization_strength = l1_regularization_strength
        self.l2_regularization_strength = l2_regularization_strength
        self.l2_shrinkage_regularization_strength =\
            l2_shrinkage_regularization_strength
        self.beta = beta
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Ftrl(
            learning_rate=self.learning_rate,
            learning_rate_power=self.learning_rate_power,
            initial_accumulator_value=self.initial_accumulator_value,
            l1_regularization_strength=self.l1_regularization_strength,
            l2_regularization_strength=self.l2_regularization_strength,
            l2_shrinkage_regularization_strength=self.l2_shrinkage_regularization_strength,  # NOQA
            beta=self.beta,
        )

    def _get_info(self) -> List[str]:
        return ['Fast', 'Single-Solution']

# =============================================================================


class Nadam(TensorflowOptimizer):
    """Nadam"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 beta_1: float = 0.9, beta_2: float = 0.999,
                 epsilon: float = 1e-07, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.Nadam(
            learning_rate=self.learning_rate,
            beta_1=self.beta_1,
            beta_2=self.beta_2,
            epsilon=self.epsilon,
        )

    def _get_info(self) -> List[str]:
        return ['Stable', 'Global', 'First-Order', 'Single-Solution']

# =============================================================================


class RMSprop(TensorflowOptimizer):
    """RMSprop"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 rho: float = 0.9, momentum: float = 0.0,
                 epsilon: float = 1e-07, centered: bool = False, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.rho = rho
        self.momentum = momentum
        self.epsilon = epsilon
        self.centered = centered
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.RMSprop(
            learning_rate=self.learning_rate,
            rho=self.rho,
            momentum=self.momentum,
            epsilon=self.epsilon,
            centered=self.centered,
        )

    def _get_info(self) -> List[str]:
        return ['Stable', 'Single-Solution']

# =============================================================================


class SGD(TensorflowOptimizer):
    """SGD"""
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.01,
                 momentum: float = 0.0, nesterov: bool = False, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.nesterov = nesterov
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = tf.keras.optimizers.SGD(
            learning_rate=self.learning_rate,
            momentum=self.momentum,
            nesterov=self.nesterov,
        )

    def _get_info(self) -> List[str]:
        return ['Stable', 'First-Order', 'Single-Solution']
