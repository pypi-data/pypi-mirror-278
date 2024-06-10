import matplotlib.pyplot as plt


class PlotBase:
    """
    Base Class for Plot

    This class serves as the parent class for any plotting of uc_sgsim package.

    Attributes:
        __figsize (tuple[int, int]): The figure size.

    Methods:
        save_plot: save current figure.
    """

    def __init__(self, figsize: tuple[int, int] = (10, 8)):
        self.__figsize = figsize

    @property
    def figsize(self) -> tuple:
        return self.__figsize

    def save_plot(self, figname: str = 'figure.png', **kwargs):
        plt.savefig(figname, **kwargs)
