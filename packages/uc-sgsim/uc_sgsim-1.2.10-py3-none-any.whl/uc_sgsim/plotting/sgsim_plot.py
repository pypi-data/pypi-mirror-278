from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from uc_sgsim.exception import VariogramDoesNotCompute
from uc_sgsim.plotting.base import PlotBase
from ..cov_model.base import CovModel


class SgsimPlot(PlotBase):
    """
    SgsimPlot Class for Visualizing Sequential Gaussian Simulation Results

    This class provides methods for visualizing results obtained from
    Sequential Gaussian Simulation (SGSIM). It includes functions for
    plotting realizations, mean plots, variance plots, cumulative distribution
    function (CDF) plots, histograms, and variograms of the simulated random fields.

    Args:
        model (CovModel): The covariance model used in the simulation.
        figsize (tuple, optional): Figure size for the plots (default is (10, 8)).

    Attributes:
        xlabel (str): Label for the x-axis in plots.
        curr_fig_num (int): Current figure number for matplotlib.

    Properties:
        vmodel (CovModel): The covariance model used in the simulation.
        vmodel_name (str): The name of the covariance model.
        vbandwidth_step (int): The bandwidth step of the covariance model.
        vbandwidth (np.array): The bandwidth of the covariance model.
        vk_range (float): The range parameter of the covariance model.
        vsill (float): The sill parameter of the covariance model.

    Methods:
        plot: Plot realizations with optional mean lines.
        mean_plot: Plot mean values of realizations.
        variance_plot: Plot variance of realizations.
        cdf_plot: Plot cumulative distribution function (CDF) for a specific location.
        hist_plot: Plot histogram for a specific location.
        variogram_plot: Plot variograms of realizations along with the theoretical variogram.
        theory_variogram_plot: Plot the theoretical variogram.
    """

    xlabel = 'Distance(-)'
    curr_fig_num = 0

    def __init__(
        self,
        model: CovModel,
        figsize: tuple = (10, 8),
    ):
        """
        Initialize an SgsimPlot object.

        Args:
            model (CovModel): The covariance model for simulation.
            figsize (tuple, optional): Figure size in inches (width, height) (default is (10, 8)).
        """
        super().__init__(figsize)
        self.__vmodel = model
        self.__vmodel_name = model.model_name
        self.__vbandwidth_step = model.bandwidth_step
        self.__vbandwidth = model.bandwidth
        self.__vk_range = model.k_range
        self.__vsill = model.sill

    @property
    def vmodel(self) -> CovModel:
        return self.__vmodel

    @property
    def vmodel_name(self) -> str:
        return self.__vmodel_name

    @property
    def vbandwidth_step(self) -> int:
        return self.__vbandwidth_step

    @property
    def vbandwidth(self) -> np.array:
        return self.__vbandwidth

    @property
    def vk_range(self) -> float:
        return self.__vk_range

    @property
    def vsill(self) -> float:
        return self.__vsill

    def plot(
        self,
        realizations: list[int] | None = None,
        mean: float | int = 0,
        fontsize: int = 20,
        y_title: str = 'Y',
        axhline_color: str = 'r',
        axhline_style: str = '--',
        axhline_zorder: int = 1,
    ) -> None:
        """
        Plot Realizations of the Random Field

        This method plots realizations of the random field with optional parameters.

        Args:
            realizations (list[int] | None, optional):
                List of realization indices to plot (default is None).
            mean (float | int, optional):
                Mean value to add to realizations (default is 0).
            fontsize (int, optional):
                Font size for labels and titles (default is 20).
            y_title (str, optional):
                Y-axis title (default is 'Y').
            axhline_color (str, optional):
                Color of the horizontal line at mean (default is 'r').
            axhline_style (str, optional):
                Linestyle of the horizontal line at mean (default is '--').
            axhline_zorder (int, optional):
                Z-order of the horizontal line at mean (default is 1).
        """
        realization_number = len(self.random_field[:, 0])
        if realizations is None:
            for i in range(realization_number):
                plt.figure(self.curr_fig_num, figsize=self.figsize)
                plt.plot(self.random_field[i, :] + mean)
                plt.title('Realizations: ' + self.vmodel_name, fontsize=fontsize)
                plt.xlabel(self.xlabel, fontsize=fontsize)
                plt.axhline(
                    y=mean,
                    color=axhline_color,
                    linestyle=axhline_style,
                    zorder=axhline_zorder,
                )
                plt.ylabel(y_title, fontsize=fontsize)
        elif isinstance(realizations, list):
            for item in realizations:
                plt.figure(self.curr_fig_num, figsize=self.figsize)
                plt.plot(self.random_field[:, item] + mean)
                plt.title('Realizations: ' + self.vmodel_name, fontsize=fontsize)
                plt.xlabel(self.xlabel, fontsize=fontsize)
                plt.axhline(
                    y=mean,
                    color=axhline_color,
                    linestyle=axhline_style,
                    zorder=axhline_zorder,
                )
                plt.ylabel(y_title, fontsize=fontsize)
        else:
            raise TypeError("Argument 'realizations' should be list or None")
        self.curr_fig_num += 1

    def mean_plot(
        self,
        mean: int | float = 0,
        fmt: str = '-s',
        linecolor: str = 'k',
        markeredgecolor: str = 'k',
        markerfacecolor: str = 'y',
        fontsize: int = 20,
        axhline_color: str = 'r',
        axhline_style: str = '--',
        axhline_zorder: int = 1,
        xticks_fontsize: int = 17,
        yticks_fontsize: int = 17,
    ) -> None:
        """
        Plot Mean of Realizations

        This method plots the mean of realizations along with optional parameters.

        Args:
            mean (int | float, optional):
                Mean value to add to realizations (default is 0).
            fmt (str, optional):
                Marker style for plotting (default is '-s').
            linecolor (str, optional):
                Color of the mean line (default is 'k').
            markeredgecolor (str, optional):
                Edge color of markers (default is 'k').
            markerfacecolor (str, optional):
                Face color of markers (default is 'y').
            fontsize (int, optional):
                Font size for labels and titles (default is 20).
            axhline_color (str, optional):
                Color of the horizontal line at mean (default is 'r').
            axhline_style (str, optional):
                Linestyle of the horizontal line at mean (default is '--').
            axhline_zorder (int, optional):
                Z-order of the horizontal line at mean (default is 1).
            xticks_fontsize (int, optional):
                Font size for x-axis tick labels (default is 17).
            yticks_fontsize (int, optional):
                Font size for y-axis tick labels (default is 17).
        """
        zmean = np.zeros(len(self.random_field[0, :]))
        for i in range(len(self.random_field[0, :])):
            zmean[i] = np.mean(self.random_field[:, i] + mean)

        plt.figure(self.curr_fig_num, figsize=self.figsize)
        plt.plot(
            zmean,
            fmt,
            color=linecolor,
            markeredgecolor=markeredgecolor,
            markerfacecolor=markerfacecolor,
        )
        plt.xlabel(self.xlabel, fontsize=fontsize)
        plt.ylabel('Mean', fontsize=fontsize)
        plt.axhline(
            y=mean,
            color=axhline_color,
            linestyle=axhline_style,
            zorder=axhline_zorder,
        )
        plt.xticks(fontsize=xticks_fontsize)
        plt.yticks(fontsize=yticks_fontsize)
        self.curr_fig_num += 1

    def variance_plot(self) -> None:
        """
        Plot Variance of Realizations

        This method plots the variance of realizations for each
        location in the random field.
        """
        zvar = np.zeros(len(self.random_field[0, :]))
        for i in range(len(self.random_field[0, :])):
            zvar[i] = np.var(self.random_field[:, i])

        plt.figure(self.curr_fig_num, figsize=self.figsize)
        plt.plot(
            zvar,
            '-o',
            color='k',
            markeredgecolor='k',
            markerfacecolor='r',
        )
        plt.xlabel(self.xlabel, fontsize=20)
        plt.ylabel('Variance', fontsize=20)
        plt.axhline(y=self.vmodel.sill, color='b', linestyle='--', zorder=1)
        plt.xticks(fontsize=17), plt.yticks(fontsize=17)
        self.curr_fig_num += 1

    def cdf_plot(self, x_location: int) -> None:
        """
        Plot Cumulative Distribution Function (CDF) for a Specific Location

        This method plots the cumulative distribution function (CDF) for the
        specified location in the random field.

        Args:
            x_location (int): The location index to plot the CDF.
        """
        x = self.random_field[:, x_location]
        mu = np.mean(x)
        sigma = np.std(x)
        n_bins = 50

        _, ax = plt.subplots(figsize=(8, 4))

        _, bins, _ = ax.hist(
            x,
            n_bins,
            density=True,
            histtype='step',
            cumulative=True,
            label='Empirical',
        )

        y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(
            -0.5 * (1 / sigma * (bins - mu)) ** 2,
        )
        y = y.cumsum()
        y /= y[-1]

        ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')

        ax.grid(True)
        ax.legend(loc='right')
        ax.set_title('Cumulative step histograms, x = ' + str(x_location))
        ax.set_xlabel('Random Variable (mm)')
        ax.set_ylabel('Occurrence')
        self.curr_fig_num += 1

    def hist_plot(self, x_location: int) -> None:
        """
        Plot Histogram for a Specific Location

        This method plots a histogram for the specified location in the random field.

        Args:
            x_location (int): The location index to plot the histogram.
        """
        x = self.random_field[:, x_location]
        mu = np.mean(x)
        sigma = np.std(x)
        num_bins = 50
        plt.figure(self.curr_fig_num)
        _, bins, _ = plt.hist(
            x,
            num_bins,
            density=1,
            color='blue',
            alpha=0.5,
            edgecolor='k',
        )

        y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(
            -0.5 * (1 / sigma * (bins - mu)) ** 2,
        )

        plt.plot(bins, y, '--', color='black')
        plt.xlabel('X-Axis')
        plt.ylabel('Y-Axis')
        plt.title('Histogram, x = ' + str(x_location))
        self.curr_fig_num += 1

    def variogram_plot(
        self,
        fontsize: int = 20,
        alpha: int | float = 0.1,
        xticks_fontsize: int = 17,
        yticks_fontsize: int = 17,
        mean_color: str = 'blue',
        mean_linestyle: str = '--',
    ) -> None:
        """
        Plot Variograms of Realizations

        This method plots variograms of realizations along with the theoretical variogram.

        Args:
            fontsize (int, optional): Font size for labels and titles (default is 20).
            alpha (int | float, optional): Transparency level for variogram lines (default is 0.1).
            xticks_fontsize (int, optional): Font size for x-axis tick labels (default is 17).
            yticks_fontsize (int, optional): Font size for y-axis tick labels (default is 17).
            mean_color (str, optional): Color for the mean line (default is 'blue').
            mean_linestyle (str, optional): Linestyle for the mean line (default is '--').
        """
        self.__variogram_validate()
        for i in range(self.realization_number):
            plt.figure(self.curr_fig_num, figsize=(10, 6))
            plt.plot(self.variogram[i, :], alpha=alpha)
            plt.title('Model: ' + self.vmodel_name, fontsize=fontsize)
            plt.xlabel('Lag(m)', fontsize=fontsize)
            plt.ylabel('Variogram', fontsize=fontsize)
            plt.xticks(fontsize=xticks_fontsize)
            plt.yticks(fontsize=yticks_fontsize)

        self.theory_variogram_plot()

        Vario_mean = np.zeros(len(self.vbandwidth))
        for i in range(len(self.vbandwidth)):
            Vario_mean[i] = np.mean(self.variogram[:, i])

        plt.plot(Vario_mean, mean_linestyle, color=mean_color)
        self.curr_fig_num += 1

    def theory_variogram_plot(
        self,
        fig: int = None,
        fontsize: int = 20,
        fmt: str = 'o',
        markeredgecolor: str = 'k',
        markerfacecolor: str = 'w',
    ) -> None:
        """
        Plot Theoretical Variogram

        This method plots the theoretical variogram of the covariance model.

        Args:
            fig (int, optional): Figure number to use (default is None).
            fontsize (int, optional): Font size for labels and titles (default is 20).
            fmt (str, optional): Marker style for plotting (default is 'o').
            markeredgecolor (str, optional): Edge color of markers (default is 'k').
            markerfacecolor (str, optional): Face color of markers (default is 'w').
        """
        if fig is not None:
            plt.figure(fig, figsize=self.figsize)
        plt.plot(
            self.vmodel.var_compute(self.vbandwidth),
            fmt,
            markeredgecolor=markeredgecolor,
            markerfacecolor=markerfacecolor,
        )
        plt.title('Model: ' + self.vmodel_name, fontsize=fontsize)
        plt.xlabel('Lag(m)', fontsize=fontsize)
        plt.ylabel('Variogram', fontsize=fontsize)

    def __variogram_validate(self) -> None:
        if isinstance(self.variogram, int):
            raise VariogramDoesNotCompute()
