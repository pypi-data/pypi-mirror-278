from __future__ import annotations

import time
import sys
from pathlib import Path
from ctypes import CDLL, POINTER, c_double, c_int
from multiprocessing import Pool

import numpy as np
from uc_sgsim.random_field import SgsimField
from uc_sgsim.cov_model.base import CovModel
from uc_sgsim.utils import CovModelStructure, SgsimStructure
from .exception import IterationError

BASE_DIR = Path(__file__).resolve().parent


class UCSgsim(SgsimField):
    """
    UnConditional Sequential Gaussian Simulation (UCSgsim) Class

    This class provides functionality for generating unconditional random fields
    using Sequential Gaussian Simulation. It supports both simple and ordinary
    kriging methods, as well as parallel processing for efficiency.

    Attributes:
        grid_size (int | list[int, int]): Size of the grid for the random field.
        model (CovModel): The covariance model for simulation.
        realization_number (int): Number of realizations to generate.
        kriging (str | Kriging): The kriging method to use ('SimpleKriging' or 'OrdinaryKriging').
        randomseed (int): Seed for random number generation.
        n_process (int): Number of parallel processes to use.
        max_neighbor (int): Maximum number of neighbors to consider.
        z_min (float): Minimum allowable value for simulated data.
        z_max (float): Maximum allowable value for simulated data.
        constant_path (bool): Flag to use a constant path for each realization.
        random_field (np.array): Array to store the generated random field.
        variogram (np.array): Array to store the computed variogram.

    Methods:
        _process(randomseed: int = 0, parallel: bool = False) -> np.array:
            Perform the simulation process for a subset of realizations.

        compute(n_process: int, randomseed: int) -> np.array:
            Generate random field realizations using parallel processing.

        variogram_compute(n_process: int = 1) -> None:
            Compute the variogram of the generated random field using parallel processing.
    """

    def _process(self, randomseed: int = 0, parallel: bool = False) -> np.array:
        """
        Perform the simulation process for a subset of realizations.

        Args:
            randomseed (int, optional): Seed for random number generation (default is 0).
            parallel (bool, optional): Flag to enable parallel processing (default is False).

        Returns:
            np.array: Array containing generated random field realizations.
        """
        self.randomseed = randomseed
        np.random.seed(self.randomseed)
        self.n_process = 1 if parallel is False else self.n_process
        counts = 0
        iteration_failed = 0
        start_time = time.time()

        # Loop for randomfield generation
        while counts < (self.realization_number // self.n_process):
            # Grid and initial value preparing
            drop = False
            unsampled = np.linspace(1, self.x_size - 2, self.x_size - 2)
            z_value = np.random.normal(0, self.model.sill**0.5, 2).reshape(2, 1)
            x_grid = np.array([0, self.x_size - 1]).reshape(2, 1)
            z = np.zeros(self.x_size)
            z[0], z[-1] = z_value[0], z_value[1]
            neighbor = 0
            grid = np.hstack([x_grid, z_value])

            # If simulate with constant_path then draw randompath only once
            if not self.constant_path or counts == 0:
                randompath = np.random.choice(
                    unsampled,
                    len(unsampled),
                    replace=False,
                )

            # Loop for kriging simulation
            for i in range(len(unsampled)):
                sample = int(randompath[i])
                z[sample] = self.kriging.simulation(
                    grid,
                    sample,
                    neighbor=neighbor,
                )

                # If any simulated value over the limit than discard that realization
                if z[sample] >= self.z_max or z[sample] <= self.z_min:
                    drop = True
                    iteration_failed += 1
                    if iteration_failed >= self.iteration_limit:
                        raise IterationError()
                    break

                temp = np.hstack([sample, z[sample]])
                grid = np.vstack([grid, temp])

                if neighbor < self.max_neighbor:
                    neighbor += 1
            self.randomseed += 1

            # IF drop is False then proceed to next realization generation
            if drop is False:
                self.random_field[counts, :] = z
                counts = counts + 1
                iteration_failed = 0
                # Set cov_cache flag to False to ensure cov_cache only compute once
                self.kriging._cov_cache_flag = False
            print('Progress = %.2f' % (counts / self.realization_number * 100) + '%', end='\r')

        print('Progress = %.2f' % 100 + '%\n', end='\r')
        end_time = time.time()
        print('Time = %f' % (end_time - start_time), 's\n')

        return self.random_field

    def compute(self, n_process: int, randomseed: int) -> np.array:
        """
        Generate random field realizations.

        Args:
            n_process (int): Number of parallel processes to use.
            randomseed (int): Seed for random number generation.

        Returns:
            np.array: Array containing generated random field realizations.
        """
        # Create pool and distribute realizations to each process.
        pool = Pool(processes=n_process)
        self.n_process = n_process
        self.realization_number = self.realization_number * n_process
        self.random_field = np.empty([self.realization_number, self.x_size])

        # Prepare the args for each processes
        rand_list = [randomseed + i for i in range(n_process)]
        parallel = [True] * n_process

        # Start parallel computing
        try:
            z = pool.starmap(self._process, zip(rand_list, parallel))
        except IterationError:
            # We should handle the error like this to measure the coverage of sub process
            pool.close()
            pool.join()
            raise IterationError()

        pool.close()
        # Use pool.join() to measure the coverage of sub process
        pool.join()

        # Collect data from each process
        for i in range(n_process):
            start = int(i * self.realization_number / n_process)
            end = int((i + 1) * self.realization_number / n_process)
            self.random_field[start:end, :] = z[i][: end - start, :]

        return self.random_field

    def variogram_compute(self, n_process: int = 1) -> None:
        """
        Compute the variogram of the generated random field.

        Args:
            n_process (int, optional): Number of parallel processes to use (default is 1).
        """
        # Create pool and args than distribute realizations and args to each process.
        pool = Pool(processes=n_process)
        model_len = self.x_size
        x = np.linspace(0, self.x_size - 1, model_len).reshape(model_len, 1)
        grid = [
            np.hstack([x, self.random_field[i, :].reshape(model_len, 1)])
            for i in range(self.realization_number)
        ]

        # Start computing
        self.variogram = pool.starmap(self.model.variogram, zip(grid))
        pool.close()
        # Use pool.join() to measure the coverage of sub process
        pool.join()
        self.variogram = np.array(self.variogram)


class UCSgsimDLL(UCSgsim):
    """
    Unconditional Sequential Gaussian Simulation (UCSgsim) with Dynamic Link Library (DLL) Support.

    This class extends the UCSgsim class to provide support for using a dynamic link library (DLL)
    for faster computation of sequential Gaussian simulation. It allows users to specify the DLL
    kriging method and utilizes parallel processing for efficiency.

    Methods:
        _lib_read() -> CDLL:
            Read and load the appropriate DLL based on the operating system.

        _cpdll(randomseed: int) -> np.array:
            Perform simulation using the specified DLL kriging method.

        compute(n_process: int, randomseed: int) -> np.array:
            Generate random field realizations using parallel processing with DLL support.

        _variogram_cpdll(n_process: int) -> np.array:
            Compute the variogram of the generated random field using parallel
            processing with DLL support.

        variogram_compute(n_process: int = 1) -> np.array:
            Compute the variogram of the generated random field using parallel processing.
    """

    def __init__(
        self,
        x: int,
        realization_number: int,
        model: CovModel,
        kriging: str = 'SimpleKriging',
        **kwargs,
    ):
        """
        Initialize a UCSgsimDLL object.

        Args:
            x (int): Size of the x-axis for the random field.
            realization_number (int): Number of realizations to generate.
            model (CovModel): The covariance model for simulation.
            kriging (str, optional):
                The DLL kriging method to use ('SimpleKriging' or 'OrdinaryKriging').
            **kwargs: Additional keyword arguments for customization.
        """
        super().__init__(x, realization_number, model, **kwargs)
        self.kriging = kriging

    def _lib_read(self) -> CDLL:
        if sys.platform.startswith('linux'):
            lib = CDLL(str(BASE_DIR) + r'/c_core/uc_sgsim.so')
        elif sys.platform.startswith('win32'):
            lib = CDLL(str(BASE_DIR) + r'/c_core/uc_sgsim.dll', winmode=0)
        return lib

    def _cpdll(self, randomseed: int) -> np.array:
        """
        Perform simulation using the specified DLL kriging method.

        Args:
            randomseed (int): Seed for random number generation.

        Returns:
            np.array: Array containing generated random field realizations.
        """
        # Read dynamic link lib and prepare arguments
        lib = self._lib_read()
        mlen = int(self.x_size)
        realization_number = int(self.realization_number // self.n_process)
        random_field = np.empty([realization_number, self.x_size])
        kriging = 1 if self.kriging == 'OrdinaryKriging' else 0

        # Create sgsim and cov structure for dynamic link lib input
        sgsim_s = SgsimStructure(
            x_len=mlen,
            realization_numbers=realization_number,
            randomseed=randomseed,
            kirging_method=kriging,
            if_alloc_memory=0,
            max_iteration=self.iteration_limit,
            array=(c_double * (mlen * realization_number))(),
            z_min=self.z_min,
            z_max=self.z_max,
        )
        cov_s = CovModelStructure(
            bw_l=self.model.bandwidth_len,
            bw_s=self.model.bandwidth_step,
            bw=self.model.bandwidth_len // self.model.bandwidth_step,
            max_neighbor=self.max_neighbor,
            use_cov_cache=0 if self.constant_path is False else 1,
            range=self.model.k_range,
            sill=self.model.sill,
            nugget=self.model.nugget,
        )

        # Run simulation with dynamic link lib
        sgsim = lib.sgsim_run
        sgsim.argtypes = (POINTER(SgsimStructure), POINTER(CovModelStructure), c_int)
        sgsim(sgsim_s, cov_s, 0)

        # Collect results into a Python-List (random_field)
        for i in range(realization_number):
            random_field[i, :] = sgsim_s.array[i * mlen : (i + 1) * mlen]
        return random_field

    def compute(self, n_process: int, randomseed: int) -> np.array:
        """
        Generate random field realizations with DLL support.

        Args:
            n_process (int): Number of parallel processes to use.
            randomseed (int): Seed for random number generation.

        Returns:
            np.array: Array containing generated random field realizations.
        """
        # Create a pool of processes and prepare the necessary arguments.
        # Then, distribute realizations and arguments to each process.
        pool = Pool(processes=n_process)
        self.n_process = n_process
        if n_process > 1:
            self.realization_number = self.realization_number * n_process
        self.random_field = np.empty([self.realization_number, self.x_size])
        rand_list = [randomseed + i for i in range(n_process)]

        # Run parallel computing with dynamic link lib
        z = pool.starmap(self._cpdll, zip(rand_list))
        pool.close()
        # Use pool.join() to measure the coverage of sub process
        pool.join()

        # Collect results into a Python-List (random_field)
        for i in range(n_process):
            start = int(i * self.realization_number / n_process)
            end = int((i + 1) * self.realization_number / n_process)
            self.random_field[start:end, :] = z[i][: end - start, :]

        return self.random_field

    def _variogram_cpdll(self, n_process: int) -> np.array:
        # Read dynamic link lib and prepare arguments
        lib = self._lib_read()
        mlen = int(self.x_size)
        realization_number = int(self.realization_number // self.n_process)
        vario_size = len(self.bandwidth)
        vario_array = (c_double * (vario_size))()
        random_field_array = (c_double * (mlen))()
        variogram = np.empty([realization_number, vario_size])

        # Set function arguments and return type for ctypes
        vario = lib.variogram
        vario.argtypes = (
            POINTER(c_double),
            POINTER(c_double),
            c_int,
            c_int,
            c_int,
        )
        vario.restype = None

        # Run variogram computing with dynamic link lib and save results as a Python-List.
        for i in range(realization_number):
            random_field_array[:] = self.random_field[i + n_process * realization_number, :]
            vario(random_field_array, vario_array, mlen, vario_size, 1)
            variogram[i, :] = list(vario_array)

        return variogram

    def variogram_compute(self, n_process: int = 1) -> np.array:
        """
        Compute the variogram of the generated random field with DLL support.

        Args:
            n_process (int, optional): Number of parallel processes to use (default is 1).
        """
        # Create a pool of processes and prepare the necessary arguments.
        # Then, distribute realizations and arguments to each process.
        pool = Pool(processes=n_process)
        self.n_process = n_process
        self.variogram = np.empty([self.realization_number, len(self.bandwidth)])
        cpu_number = [i for i in range(self.n_process)]

        # Run parallel computing with dynamic link lib
        z = pool.starmap(self._variogram_cpdll, zip(cpu_number))
        pool.close()
        # Use pool.join() to measure the coverage of sub process
        pool.join()

        # Collect results into a Python-List (random_field)
        for i in range(n_process):
            for j in range(int(self.realization_number / n_process)):
                self.variogram[(j + int(i * self.realization_number / n_process)), :] = z[i][j, :]
        return self.variogram
