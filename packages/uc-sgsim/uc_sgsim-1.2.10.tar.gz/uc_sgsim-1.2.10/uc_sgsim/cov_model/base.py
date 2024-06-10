import numpy as np
from scipy.spatial.distance import cdist


class CovModel:
    """
    Covariance Model for Sequential Gaussian Simulation.

    This class represents a covariance model used in Sequential Gaussian Simulation
    for geostatistical simulations. It defines the spatial correlation structure based on
    variogram modeling.

    Attributes:
        __bandwidth_len (float): The length of the bandwidth.
        __bandwidth_step (float): The step size for bandwidth increments.
        __bandwidth (np.array): An array of bandwidth values.
        __k_range (float): The range parameter for the covariance model.
        __sill (float): The sill parameter for the covariance model.
        __nugget (float): The nugget effect parameter for the covariance model.

    Methods:
        cov_compute(x: np.array) -> np.array: Compute covariance values.
        var_compute(x: np.array) -> np.array: Compute variogram values.
        variogram(x: np.array) -> np.array: Compute variogram for a given dataset.
        variogram_plot(fig: int = None): Plot theoretical variogram using SgsimPlot.
    """

    def __init__(
        self,
        bandwidth_len: float,
        bandwidth_step: float,
        k_range: float,
        sill: float = 1,
        nugget: float = 0,
    ):
        """
        Initialize a CovModel object.

        Args:
            bandwidth_len (float): The length of the bandwidth.
            bandwidth_step (float): The step size for bandwidth increments.
            k_range (float): The range parameter for the covariance model.
            sill (float, optional): The sill parameter for the covariance model (default is 1).
            nugget (float, optional): The nugget effect parameter for the covariance model
                                      (default is 0).
        """
        self.__bandwidth_len = bandwidth_len
        self.__bandwidth_step = bandwidth_step
        self.__bandwidth = np.arange(0, bandwidth_len, bandwidth_step)
        self.__k_range = k_range
        self.__sill = sill
        self.__nugget = nugget

    @property
    def bandwidth_len(self) -> float:
        return self.__bandwidth_len

    @property
    def bandwidth_step(self) -> float:
        return self.__bandwidth_step

    @property
    def bandwidth(self) -> np.array:
        return self.__bandwidth

    @property
    def k_range(self) -> float:
        return self.__k_range

    @property
    def sill(self) -> float:
        return self.__sill

    @property
    def nugget(self) -> float:
        return self.__nugget

    def __repr__(self) -> str:
        return (
            f'{self.model_name}Model(bandwidth_len={self.bandwidth_len}, '
            + f'bandwidth_step={self.bandwidth_step}, '
            + f'k_range={self.k_range}, sill={self.sill}, nugget={self.nugget})'
        )

    def cov_compute(self, x: np.array) -> np.array:
        """
        Compute covariance values for a given dataset.

        Args:
            x (np.array): Input dataset for which covariance values are computed.

        Returns:
            np.array: Array of covariance values.
        """
        cov = np.empty(len(x))
        for i in range(len(x)):
            cov[i] = self.__sill - self.model(x[i])

        return cov

    def var_compute(self, x: np.array) -> np.array:
        """
        Compute variance values for a given dataset.

        Args:
            x (np.array): Input dataset for which variance values are computed.

        Returns:
            np.array: Array of variance values.
        """
        var = np.empty(len(x))
        for i in range(len(x)):
            var[i] = self.model(x[i])

        return var

    def variogram(self, x: np.array) -> np.array:
        """
        Compute variogram for a given dataset.

        Args:
            x (np.array): Input dataset for which the variogram is computed.

        Returns:
            np.array: Array of variogram values.
        """
        dist = cdist(x[:, :1], x[:, :1])
        variogram = []

        for h in self.__bandwidth:
            indices = np.where(
                (dist >= h - self.__bandwidth_step) & (dist <= h + self.__bandwidth_step),
            )
            z = np.power(x[indices[0], 1] - x[indices[1], 1], 2)
            z_sum = np.sum(z)
            if z_sum >= 1e-7:
                variogram.append(z_sum / (2 * len(z)))

        return np.array(variogram)

    def variogram_plot(self, fig: int = None):
        """
        Plot the theoretical variogram using SgsimPlot.

        Args:
            fig (int, optional): The figure number to use for plotting (default is None).
        """
        from ..plotting.sgsim_plot import SgsimPlot

        SgsimPlot(model=self).theory_variogram_plot(fig=fig)
