#                                                                       Modules
# =============================================================================

from ._src import _OPTIMIZERS
from ._src._imports import try_import

with try_import() as _evosax_imports:
    from ._src.evosax_optimizers import (EvoSaxCMAES, EvoSaxDE, EvoSaxPSO,
                                         EvoSaxSimAnneal)

with try_import() as _nevergrad_imports:
    from ._src.nevergrad_optimizers import PSO, NevergradDE

with try_import() as _pygmo_imports:
    from ._src.pygmo_optimizers import (CMAES, SADE, SEA, SGA, XNES,
                                        DifferentialEvolution, PygmoPSO,
                                        SimulatedAnnealing)

with try_import() as _optuna_imports:
    from ._src.optuna_optimizers import TPESampler

with try_import() as _tensorflow_imports:
    from ._src.tensorflow_optimizers import (SGD, Adamax, AdamTensorflow, Ftrl,
                                             Nadam, RMSprop)

with try_import() as _optax_imports:
    from ._src.optax_optimizers import Adam

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================

__all__ = [
    "_OPTIMIZERS",
    "Adam",
    "Adamax",
    "AdamTensorflow",
    "CMAES",
    "DifferentialEvolution",
    "EvoSaxCMAES",
    "EvoSaxDE",
    "EvoSaxPSO",
    "EvoSaxSimAnneal",
    "Ftrl",
    "Nadam",
    "NevergradDE",
    "PSO",
    "PygmoPSO",
    "RMSprop",
    "SADE",
    "SEA",
    "SGA",
    "SGD",
    "SimulatedAnnealing",
    "TPESampler",
    "XNES",
]

__version__ = '1.5.3'
