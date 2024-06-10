from __future__ import annotations

import numpy as np
from scipy.spatial.distance import pdist, squareform
from uc_sgsim.kriging.base import Kriging


class SimpleKriging(Kriging):
    """
    Simple Kriging Class

    This class represents the Simple Kriging interpolation technique, which is used
    to estimate values at unsampled locations based on sampled data and a specified
    covariance model.

    Attributes:
        model (CovModel): The covariance model used for interpolation.
        grid_size (int | list[int, int]): Size of the grid for interpolation.
        cov_cache (bool): Flag indicating whether to use a covariance cache.

    Methods:
        prediction(sample: np.array, unsampled: np.array) -> tuple[float, float]:
            Perform Simple Kriging prediction for an unsampled location.
        simulation(x: np.array, unsampled: np.array, **kwargs) -> float:
            Perform Simple Kriging simulation for unsampled locations.
        _find_neighbor(dist: list[float], neighbor: int) -> float:
            Find a nearby point for simulation based on a neighbor criterion.
    """

    def prediction(self, sample: np.array, unsampled: np.array) -> tuple[float, float]:
        """
        Perform Simple Kriging prediction for an unsampled location.

        Args:
            sample (np.array): Sampled data for neighboring locations.
            unsampled (np.array): Unsamped location for which prediction is made.

        Returns:
            tuple[float, float]: Estimated value and kriging standard deviation.
        """
        n_sampled = len(sample)
        dist_diff = abs(sample[:, 0] - unsampled)
        dist_diff = dist_diff.reshape(len(dist_diff), 1)

        grid = np.hstack([sample, dist_diff])
        meanvalue = 0

        if self._cov_cache_flag is True:
            cov_dist = np.array(self.model.cov_compute(grid[:, 2])).reshape(-1, 1)
            self._cov_cache[int(unsampled)] = cov_dist
        elif hasattr(self, '_cov_cache') is True:
            cov_dist = self._cov_cache[int(unsampled)]
        else:
            cov_dist = np.array(self.model.cov_compute(grid[:, 2])).reshape(-1, 1)

        cov_data = squareform(pdist(grid[:, :1])).flatten()
        cov_data = np.array(self.model.cov_compute(cov_data))
        cov_data = cov_data.reshape(n_sampled, n_sampled)
        # Add a small nugget to the diagonal of the covariance matrix for numerical stability
        cov_data[np.diag_indices_from(cov_data)] += 1e-4

        weights = np.linalg.solve(cov_data, cov_dist)
        residuals = grid[:, 1] - meanvalue
        estimation = np.dot(weights.T, residuals) + meanvalue
        kriging_var = float(self.model.sill - np.dot(weights.T, cov_dist))

        kriging_var = kriging_var if kriging_var > 0 else 0
        kriging_std = np.sqrt(kriging_var)

        return estimation, kriging_std

    def simulation(self, x: np.array, unsampled: np.array, **kwargs) -> float:
        """
        Perform Simple Kriging simulation for unsampled locations.

        Args:
            x (np.array): Sampled data for neighboring locations.
            unsampled (np.array): Unsamped location for which simulation is performed.
            neighbor (int): The number of neighbors to consider (optional).

        Returns:
            float: Simulated value for the unsampled location.
        """
        neighbor = kwargs.get('neighbor')
        if neighbor is not None:
            dist = abs(x[:, 0] - unsampled)
            dist = dist.reshape(len(dist), 1)
            has_neighbor = self._find_neighbor(dist, neighbor)
            if has_neighbor:
                return has_neighbor
            x = np.hstack([x, dist])
            sorted_indices = np.argpartition(x[:, 2], neighbor)[:neighbor]
            x = x[sorted_indices]

        estimation, kriging_std = self.prediction(x, unsampled)

        random_fix = np.random.normal(0, kriging_std, 1)
        return estimation + random_fix

    def _find_neighbor(self, dist: list[float], neighbor: int) -> float:
        """
        Find a nearby point for simulation based on a neighbor criterion.

        Args:
            dist (list[float]): Distances from sampled points to the unsampled location.
            neighbor (int): The number of neighbors to consider.

        Returns:
            float: Simulated value based on neighbors or a random value if no neighbors are found.
        """
        if neighbor == 0:
            return np.random.normal(0, self.model.sill**0.5, 1)
        close_point = 0

        criteria = self.k_range * 1.732 if self.model.model_name == 'Gaussian' else self.k_range

        for item in dist:
            if item <= criteria:
                close_point += 1

        if close_point == 0:
            return np.random.normal(0, self.model.sill**0.5, 1)


class OrdinaryKriging(SimpleKriging):
    """
    Ordinary Kriging Class

    This class represents the Ordinary Kriging interpolation technique, which is
    an extension of Simple Kriging. It is used to estimate values at unsampled
    locations based on sampled data and a specified covariance model.

    Attributes:
        model (CovModel): The covariance model used for interpolation.
        grid_size (int | list[int, int]): Size of the grid for interpolation.
        cov_cache (bool): Flag indicating whether to use a covariance cache.

    Methods:
        prediction(sample: np.array, unsampled: np.array) -> tuple[float, float]:
            Perform Ordinary Kriging prediction for an unsampled location.
        matrix_augmented(mat: np.array) -> np.array:
            Augment the covariance matrix for Ordinary Kriging.
    """

    def prediction(self, sample: np.array, unsampled: np.array) -> tuple[float, float]:
        """
        Perform Ordinary Kriging prediction for an unsampled location.

        Args:
            sample (np.array): Sampled data for neighboring locations.
            unsampled (np.array): Unsamped location for which prediction is made.

        Returns:
            tuple[float, float]: Estimated value and kriging standard deviation.
        """
        n_sampled = len(sample)
        dist_diff = abs(sample[:, 0] - unsampled)
        dist_diff = dist_diff.reshape(len(dist_diff), 1)

        grid = np.hstack([sample, dist_diff])

        if self._cov_cache_flag:
            cov_dist = np.array(self.model.cov_compute(grid[:, 2])).reshape(-1, 1)
            self._cov_cache[int(unsampled)] = cov_dist
        elif hasattr(self, '_cov_cache'):
            cov_dist = self._cov_cache[int(unsampled)]
        else:
            cov_dist = np.array(self.model.cov_compute(grid[:, 2])).reshape(-1, 1)

        cov_data = squareform(pdist(grid[:, :1])).flatten()
        cov_data = np.array(self.model.cov_compute(cov_data))
        cov_data = cov_data.reshape(n_sampled, n_sampled)

        # Add a small value to the diagonal of the covariance matrix for numerical stability
        cov_data[np.diag_indices_from(cov_data)] += 1e-4

        cov_data_augmented = self._matrix_augmented(cov_data)
        cov_dist_augmented = np.vstack((cov_dist, [1.0]))
        weights = np.linalg.solve(cov_data_augmented, cov_dist_augmented)[:n_sampled]

        estimation = np.dot(weights.T, grid[:, 1])
        kriging_var = float(self.model.sill - np.dot(weights.T, cov_dist))

        kriging_var = kriging_var if kriging_var > 0 else 0
        kriging_std = np.sqrt(kriging_var)

        return estimation, kriging_std

    def _matrix_augmented(self, mat: np.array):
        """
        Augment the covariance matrix to constrain summation of weights = 1 for Ordinary Kriging.

        Args:
            mat (np.array): Covariance matrix.

        Returns:
            np.array: Augmented covariance matrix.
        """
        ones_column = np.ones((mat.shape[0], 1))
        cov_data_augmented = np.hstack([mat, ones_column])
        ones_row = np.ones((1, cov_data_augmented.shape[1]))
        ones_row[0][-1] = 0
        cov_data_augmented = np.vstack((cov_data_augmented, ones_row))
        return cov_data_augmented
