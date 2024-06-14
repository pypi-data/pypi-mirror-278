"""
Protocol classes from types outside the optimization submodule
"""
#                                                                       Modules
# =============================================================================

from __future__ import annotations

# Standard
from typing import Dict

try:
    from typing import Protocol
except ImportError:  # Python 3.7
    from typing_extensions import Protocol

# Third-party core
import numpy as np

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


class Domain(Protocol):
    """Protocol class for the domain"""

    @property
    def continuous(self):
        ...

    def get_bounds(self) -> np.ndarray:
        ...


class ExperimentSample(Protocol):
    ...


class DataGenerator(Protocol):
    def _run(
            self,
            experiment_sample: ExperimentSample | np.ndarray | Dict) -> \
            ExperimentSample:
        ...
