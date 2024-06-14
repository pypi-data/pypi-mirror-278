#                                                                       Modules
# =============================================================================

# Standard
from typing import Tuple

# Third-party
import autograd.numpy as np

# Local
from .._protocol import DataGenerator, Domain
from ..optimizer import Optimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class NeverGradOptimizer(Optimizer):
    def __init__(self, domain: Domain, population: int):
        self.domain = domain
        self.population = population

    def update_step(self,
                    data_generator: DataGenerator) -> Tuple[np.ndarray, None]:
        x = [self.algorithm.ask() for _ in range(
            self.population)]

        # Evaluate the candidates
        y = []
        for x_i in x:
            experiment_sample = data_generator._run(x_i.value,
                                                    domain=self.domain)
            y.append(experiment_sample.to_numpy()[1])

        for x_tell, y_tell in zip(x, y):
            self.algorithm.tell(x_tell, y_tell)

        # return the data
        return np.vstack([x_.value for x_ in x]), np.array(y).ravel()
