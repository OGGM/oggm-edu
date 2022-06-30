import oggm_edu
from oggm_edu.funcs import expression_parser
import matplotlib.pyplot as plt
from numpy.testing import assert_equal
import pytest


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


def test_expression_parser():
    """Test the expression parser."""
    # Does it work like we think it does?
    assert 20 == expression_parser("*10", 2)
    assert 4 == expression_parser("+ 2", 2.0)
    assert 4.5 == expression_parser("+ 2.5", 2.0)
    assert 1 == expression_parser("/ 2", 2.0)
    assert 5 == expression_parser("", 5.0)

    # Should raise
    with pytest.raises(Exception) as e_info:
        expression_parser(" * 10", 2)
    with pytest.raises(Exception) as e_info:
        expression_parser(" * 10", "elk")
