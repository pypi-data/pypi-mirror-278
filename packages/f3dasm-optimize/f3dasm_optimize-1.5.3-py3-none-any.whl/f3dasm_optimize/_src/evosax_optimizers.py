#                                                                       Modules
# =============================================================================

# Standard
from typing import Optional

# Third-party
from evosax import BIPOP_CMA_ES, CMA_ES, DE, PSO, SimAnneal

# Local
from ._protocol import Domain
from .adapters.evosax_implementations import EvoSaxOptimizer

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class EvoSaxCMAES(EvoSaxOptimizer):
    require_gradients: bool = False

    def __init__(
        self, domain: Domain, population: int = 30, seed: Optional[int] = None,
            **kwargs):
        super().__init__(
            domain=domain, population=population, seed=seed)
        self.evosax_algorithm = CMA_ES
        self._set_algorithm()

# =============================================================================


class EvoSaxPSO(EvoSaxOptimizer):
    require_gradients: bool = False

    def __init__(
        self, domain: Domain, population: int = 30, seed: Optional[int] = None,
            **kwargs):
        super().__init__(
            domain=domain, population=population, seed=seed, **kwargs)
        self.evosax_algorithm = PSO
        self._set_algorithm()

# =============================================================================


class EvoSaxSimAnneal(EvoSaxOptimizer):
    require_gradients: bool = False

    def __init__(
        self, domain: Domain, population: int = 30, seed: Optional[int] = None,
            **kwargs):
        super().__init__(
            domain=domain, population=population, seed=seed)
        self.evosax_algorithm = SimAnneal
        self._set_algorithm()

# =============================================================================


EvoSaxDE_DEFAULTS = {'population': 30}


class EvoSaxDE(EvoSaxOptimizer):
    require_gradients: bool = False

    def __init__(
        self, domain: Domain, population: int = 30, seed: Optional[int] = None,
            **kwargs):
        super().__init__(
            domain=domain, population=population, seed=seed)
        self.evosax_algorithm = DE
        self._set_algorithm()

# =============================================================================


class EvoSaxBIPOPCMAES(EvoSaxOptimizer):
    require_gradients: bool = False

    def __init__(
        self, domain: Domain, population: int = 30, seed: Optional[int] = None,
            **kwargs):
        super().__init__(
            domain=domain, population=population, seed=seed)
        self.evosax_algorithm = BIPOP_CMA_ES
        self._set_algorithm()
