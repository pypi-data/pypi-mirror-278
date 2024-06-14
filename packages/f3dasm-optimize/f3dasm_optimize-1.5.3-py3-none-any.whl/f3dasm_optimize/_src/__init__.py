#                                                                       Modules
# =============================================================================

# Standard

from ._imports import try_import

with try_import() as _evosax_imports:
    from .evosax_optimizers import (EvoSaxCMAES, EvoSaxDE, EvoSaxPSO,
                                    EvoSaxSimAnneal)

with try_import() as _nevergrad_imports:
    from .nevergrad_optimizers import PSO, NevergradDE

with try_import() as _pygmo_imports:
    from .pygmo_optimizers import (CMAES, SADE, SEA, SGA, XNES,
                                   DifferentialEvolution, PygmoPSO,
                                   SimulatedAnnealing)

with try_import() as _optuna_imports:
    from .optuna_optimizers import TPESampler

with try_import() as _tensorflow_imports:
    from .tensorflow_optimizers import (SGD, Adamax, AdamTensorflow, Ftrl,
                                        Nadam, RMSprop)

with try_import() as _optax_imports:
    from .optax_optimizers import Adam

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


_OPTIMIZERS = []

if _pygmo_imports.is_successful():
    _OPTIMIZERS.extend([CMAES, PygmoPSO, SADE, SEA, SGA, XNES,
                        DifferentialEvolution, SimulatedAnnealing])

if _optuna_imports.is_successful():
    _OPTIMIZERS.extend([TPESampler])

if _tensorflow_imports.is_successful():
    _OPTIMIZERS.extend([SGD, AdamTensorflow, Adamax, Ftrl, Nadam, RMSprop])

if _evosax_imports.is_successful():
    _OPTIMIZERS.extend([EvoSaxPSO, EvoSaxSimAnneal, EvoSaxDE,
                        EvoSaxCMAES])

if _nevergrad_imports.is_successful():
    _OPTIMIZERS.extend([NevergradDE, PSO])

if _optax_imports.is_successful():
    _OPTIMIZERS.extend([Adam])

__all__ = [
    'AdamTensorflow',
    'Adamax',
    'CMAES',
    'DifferentialEvolution',
    'EvoSaxCMAES',
    'EvoSaxDE',
    'EvoSaxPSO',
    'EvoSaxSimAnneal',
    'EvoSaxBIPOPCMAES',
    'Ftrl',
    'MMA',
    'Nadam',
    'NevergradDE',
    'PSO',
    'PygmoPSO',
    'RMSprop',
    'SADE',
    'SEA',
    'SGA',
    'SGD',
    'SimulatedAnnealing',
    'XNES',
    'TPESampler',
    'Adam',
    '__version__',
]
