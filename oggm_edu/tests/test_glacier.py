from oggm_edu import Glacier, SurgingGlacier, GlacierBed, MassBalance
import numpy as np
from numpy.testing import assert_equal
from matplotlib import pyplot as plt
import pytest

real_mb = MassBalance(ela=3000, gradient=5)
real_bed = GlacierBed(top=3400, bottom=1500, width=500)


def test_glacier_constructor():
    """The glacier consructor is fairly simple, we only check that exceptions are raised."""

    with pytest.raises(Exception) as e_info:
        fake_bed = ["hello"]
        Glacier(bed=fake_bed, mass_balance=real_mb)
    with pytest.raises(Exception) as e_info:
        fake_mb = 21654
        Glacier(bed=real_bed, mass_balance=fake_mb)

    # Initial glacier height should match bed height.
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    assert_equal(glacier.surface_h, real_bed.bed_h)


def test_copy():
    """Is copy really producing a copy?"""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)

    glacier_copy = glacier.copy()

    assert glacier != glacier_copy
    assert isinstance(glacier_copy, Glacier)

    # Change attribute of the copy and make sure that it is only changed of the copy.
    # Should be the same value here.
    assert glacier_copy.ela == glacier.ela
    glacier_copy.mass_balance.ela = 3200
    # But not any longer.
    assert glacier_copy.ela != glacier.ela


def test_progress_to_year():
    """Test the method progress_to_year."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)

    # Progress the glacier.
    year = 50
    glacier.progress_to_year(year)

    # This will progress the glacier normally and relies on
    # oggm.FluxBasedModel for run and store.
    assert glacier.age == year
    # Length of history will be 1 longer since we include the 0 year.
    assert len(glacier.history.time) == year + 1
    assert glacier.history.time.isel(time=-1) == year
    # State history appending should work as well.
    assert len(glacier.state_history.time) == year + 1

    # Progress a bit further, checks that appending to history works as intended.
    year = 60
    glacier.progress_to_year(year)
    assert glacier.age == year
    # Length of history will be 1 longer since we include the 0 year.
    assert len(glacier.history.time) == year + 1
    assert glacier.history.time.isel(time=-1) == year
    assert len(glacier.state_history.time) == year + 1


# Some fancy plot testing.
@pytest.mark.mpl_image_compare(
    baseline_dir="baseline_images", filename="glacier_plot.png"
)
def test_plot():
    """Make sure the base plot look as intended."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    # Plot the glacier.
    glacier.plot()
    # Retreive the figure.
    fig = plt.gcf()
    return fig


@pytest.mark.mpl_image_compare(
    baseline_dir="baseline_images", filename="mass_balance_plot.png"
)
def test_plot_mass_balance():
    """Make sure the mass_balance plot look as intended."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    # Plot the glacier.
    glacier.plot_mass_balance()
    # Retreive the figure.
    fig = plt.gcf()
    return fig


@pytest.mark.mpl_image_compare(
    baseline_dir="baseline_images", filename="history_plot.png"
)
def test_plot_history():
    """Make sure the mass_balance plot look as intended."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    glacier.progress_to_year(100)
    # Plot the glacier.
    fig, _, _, _ = glacier._create_history_plot_components()

    return fig


@pytest.mark.mpl_image_compare(
    baseline_dir="baseline_images", filename="state_history_plot.png"
)
def test_plot_state_history():
    """Make sure the mass_balance plot look as intended."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    glacier.progress_to_year(100)
    # Plot the glacier.
    glacier.plot_state_history()

    fig = plt.gcf()

    return fig


def test_surging_glacier():
    """Some test on the surging glacier."""

    surging_glacier = SurgingGlacier(bed=real_bed, mass_balance=real_mb)

    # Progress the surging glacier
    year = 200
    surging_glacier.progress_to_year(year)

    assert surging_glacier.age == year
    # A full cycle is 55 years for default surging glacier. Four full cycles is 220 years,
    # and a surging cycle is 5 years: 15 normal years left.
    assert surging_glacier._normal_years_left == 15
    assert surging_glacier._surging_years_left == 5

    # Is surging mechanism working?
    # At least we can check that length increase when surging starts
    len_before_surge = surging_glacier.history.sel(time=104).length_m.values
    len_during_surge = surging_glacier.history.sel(time=108).length_m.values

    # A bit bit simple, but length should increase during a surge.
    assert len_before_surge < len_during_surge

    # No eq. state method.
    with pytest.raises(Exception) as e_info:
        surging_glacier.progress_to_equilibrium()


# Test the plotting.
@pytest.mark.mpl_image_compare(
    baseline_dir="baseline_images", filename="surging_history_plot.png"
)
def test_surging_history_plot():
    surging_glacier = SurgingGlacier(bed=real_bed, mass_balance=real_mb)

    # Progress the surging glacier
    year = 200
    surging_glacier.progress_to_year(year)
    surging_glacier.plot_history()
    fig = plt.gcf()
    return fig
