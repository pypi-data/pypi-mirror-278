#                                                                       Modules
# =============================================================================

# Third-party
import optax

# Local
from ._protocol import Domain
from .adapters.optax_implementations import OptaxOptimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class Adam(OptaxOptimizer):
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.001,
                 beta_1: float = 0.9, beta_2: float = 0.999,
                 epsilon: float = 1e-07, eps_root: float = 0.0, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.beta_1 = beta_1
        self.beta_2 = beta_2
        self.epsilon = epsilon
        self.eps_root = eps_root
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = optax.adam(
            learning_rate=self.learning_rate,
            b1=self.beta_1,
            b2=self.beta_2,
            eps=self.epsilon,
            eps_root=self.eps_root
        )


# =============================================================================


class SGDOptax(OptaxOptimizer):
    require_gradients: bool = True

    def __init__(self, domain: Domain, learning_rate: float = 0.01,
                 momentum: float = 0.0, nesterov: bool = False, **kwargs):
        super().__init__(domain=domain)
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.nesterov = nesterov
        self._set_algorithm()

    def _set_algorithm(self):
        self.algorithm = optax.sgd(
            learning_rate=self.learning_rate,
            momentum=self.momentum,
            nesterov=self.nesterov
        )


# =============================================================================
