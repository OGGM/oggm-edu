from oggm.cfg import SEC_IN_YEAR
from oggm_edu import MassBalance
import numpy as np
import pandas as pd
from numpy.testing import assert_equal
import pytest


def test_constructor():
    mb = MassBalance(ela=2000, gradient=[10, 5], breakpoints=[2000])

    # Does assignment work?
    assert mb.grad == [10, 5]

    mb = MassBalance(ela=2000, gradient=10)
    assert mb.grad == 10
    assert mb.ela_h == 2000
    assert mb.orig_ela_h == 2000
    assert mb.temp_bias == 0

    # We are not allowed to pass negative gradients.
    with pytest.raises(Exception) as e_info:
        mb = MassBalance(ela=2000, gradient=[10, -5], breakpoints=[2000])


def test_temp_bias():
    """Test temp bias"""
    mb = MassBalance(ela=2000, gradient=10)

    mb.temp_bias = 1

    assert mb.temp_bias == 1
    assert mb.ela_h == mb.orig_ela_h + 150


def test_gradient_lookup():
    """Test the gradient lookup function"""
    # Fancy case
    mb = MassBalance(ela=2000, gradient=[10, 5], breakpoints=[2000])

    # Computed gradients
    heights = [3000, 2500, 2000, 1500, 1000]
    computed_grads = mb._gradient_lookup(heights)
    # Correct grads
    corr_grads = [10, 10, 5, 5, 5]

    assert_equal(computed_grads, corr_grads)
    # Simple case
    mb = MassBalance(ela=2000, gradient=10)

    # Computed gradients
    computed_grads = mb._gradient_lookup(heights)
    # Correct grads
    corr_grads = [10, 10, 10, 10, 10]

    assert_equal(computed_grads, corr_grads)


def test_get_annual_mb():
    """Test the annual mb computation"""
    # Non-linear mass balance
    mb = MassBalance(ela=2000, gradient=[10, 5], breakpoints=[2000])

    heights = [3000, 2500, 2000, 1500, 1000]

    computed_mbs = mb.get_annual_mb(heights)

    corr_mbs = (
        np.array([1000 * 10, 500 * 10, 0, -500 * 5, -1000 * 5]) / SEC_IN_YEAR / mb.rho
    )
    assert_equal(computed_mbs, corr_mbs)
    # Another non-linear mb.
    # Breakpoints and heights does not have to match for it to work.
    mb = MassBalance(ela=2000, gradient=[10, 5, 3], breakpoints=[2000, 1200])

    computed_mbs = mb.get_annual_mb(heights)

    # INtersection
    m = (1200 - 2000) * (5 - 3)
    corr_mbs = (
        np.array([1000 * 10, 500 * 10, 0, -500 * 5, -1000 * 3 + m])
        / SEC_IN_YEAR
        / mb.rho
    )
    assert_equal(computed_mbs, corr_mbs)

    # Liner mass balance.
    mb = MassBalance(ela=2000, gradient=10)

    corr_mbs = (np.asarray(heights) - 2000) * 10 / SEC_IN_YEAR / mb.rho

    computed_mbs = mb.get_annual_mb(heights)

    assert_equal(corr_mbs, computed_mbs)


def test_temp_bias_setter():
    """Test the setter of the temp_bias_series."""
    mb = MassBalance(ela=2000, gradient=10)

    # Check year dtype
    data = ["1", "hello", "2"]
    with pytest.raises(Exception) as e_info:
        mb.temp_bias_series = data

    # Finally something that should work.
    data = [1, 1.5, 1]
    mb.temp_bias_series = data
    assert len(mb.temp_bias_series.year) == 4
    assert_equal(mb.temp_bias_series.bias, np.array([0, 1, 1.5, 1]))
