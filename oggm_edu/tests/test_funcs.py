import oggm_edu
import matplotlib.pyplot as plt
from numpy.testing import assert_equal


def test_plot_glacier_graphics():
    ax = oggm_edu.plot_glacier_graphics()
    assert ax


def test_edu_plotter_decorator():
    @oggm_edu.funcs.edu_plotter
    def plot_sth():
        f, ax = plt.subplots()
        ax.plot([1, 2, 3])
        ax.set_title("My test title")
        return ax

    ax = plot_sth(figsize=(16, 16))
    assert_equal(ax.get_figure().get_size_inches(), [16.0, 16.0])
