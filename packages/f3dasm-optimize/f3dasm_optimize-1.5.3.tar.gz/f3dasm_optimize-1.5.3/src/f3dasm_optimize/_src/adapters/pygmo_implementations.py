#                                                                       Modules
# =============================================================================

# Standard
from typing import List, Optional, Tuple

# Third-party core
import autograd.numpy as np
import pygmo as pg

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


class _PygmoProblem:
    """Convert a testproblem from the problemset to pygmo object

    Parameters
    ----------
    domain
        domain to be used
    func
        function to be evaluated
    seed
        seed for the random number generator
        _description_
    """

    def __init__(self, domain: Domain,
                 func: DataGenerator, seed: Optional[int] = None):
        self.domain = domain
        self.func = func
        self.seed = seed

        if self.seed is not None:
            pg.set_global_rng_seed(self.seed)

    def fitness(self, x: np.ndarray) -> np.ndarray:
        """Pygmo representation of returning the objective value of a function

        Parameters
        ----------
        x
            input vector

        Returns
        -------
            fitness
        """
        evaluated_sample = self.func._run(x, domain=self.domain)
        _, y_ = evaluated_sample.to_numpy()
        return y_.ravel()  # pygmo doc: should output 1D numpy array

    def batch_fitness(self, x: np.ndarray) -> np.ndarray:
        """Pygmo representation of returning multiple objective
        values of a function

        Parameters
        ----------
        x
            input vectors

        Returns
        -------
            fitnesses
        """
        # Pygmo representation of returning multiple
        # objective values of a function
        return self.fitness(x)

    def get_bounds(self) -> Tuple[List[float], List[float]]:
        """Box-constrained boundaries of the problem.
        Necessary for pygmo library

        Returns
        -------
            box constraints
        """
        bounds = self.domain.get_bounds()
        return bounds[:, 0].tolist(), bounds[:, 1].tolist()


class PygmoAlgorithm(Optimizer):
    """Wrapper around the pygmo algorithm class

    Parameters
    ----------
    data
        ExperimentData-object
    hyperparameters
        Dictionary with hyperparameters
    seed
        seed to set the optimizer
    defaults
        Default hyperparameter arguments
    """

    def __init__(self, domain: Domain, population: int,
                 seed: Optional[int]):

        if seed is None:
            seed = np.random.randint(1e6)

        self.domain = domain
        self.seed = seed
        self.population = population

        pg.set_global_rng_seed(seed=self.seed)

    def _construct_model(self, data_generator: DataGenerator):
        # Construct the PygmoProblem
        prob = pg.problem(
            _PygmoProblem(
                domain=self.domain,
                func=data_generator,
                seed=self.seed,
            )
        )

        # Construct the population
        self.pop = pg.population(prob, size=self.population)

    def update_step(
            self,
            data_generator: DataGenerator) -> Tuple[np.ndarray, np.ndarray]:
        """Update step of the algorithm

        Parameters
        ----------
        function
            function to be evaluated

        Returns
        -------
            tuple of updated input parameters (x) and objecti value (y)
        """
        # # Construct the PygmoProblem
        # prob = pg.problem(
        #     _PygmoProblem(
        #         domain=self.domain,
        #         func=data_generator,
        #         seed=self.seed,
        #     )
        # )

        # # Construct the population
        # pop = pg.population(prob, size=self.population)

        # Set the population to the latest datapoints
        pop_x = self.data._input_data.to_dataframe(
        ).iloc[-self.population:].to_numpy()
        pop_fx = self.data._output_data.to_dataframe(
        ).iloc[-self.population:].to_numpy()

        for index, (x, fx) in enumerate(zip(pop_x, pop_fx)):
            self.pop.set_xf(index, x, fx)

        # Iterate one step
        self.pop = self.algorithm.evolve(self.pop)

        # return the data
        return self.pop.get_x(), self.pop.get_f()
