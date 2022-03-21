from oggm_edu import Glacier, SurgingGlacier, GlacierBed, MassBalance
from numpy.testing import assert_equal
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


def test_progress_to_equilibrium():
    """Should be possible to combine progress_to_year and progress_to_equilibrium"""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    glacier.progress_to_year(100)
    glacier.progress_to_equilibrium()

    # We don't really now what the eq state is. But at least some checks on the data.
    assert len(glacier.history.time) == len(glacier.state_history.time)


def test_add_temperature_bias():
    """Test to make sure that the entire temperature bias mechanism works as intended."""
    glacier = Glacier(bed=real_bed, mass_balance=real_mb)
    # Add a temperature bias
    duration = 10
    bias = 2.0
    glacier.add_temperature_bias(bias=2.0, duration=duration)
    # Progress the glacier a few years.
    year = 2
    glacier.progress_to_year(year)
    # Check the current temperature bias.
    assert glacier.mass_balance.temp_bias == bias / duration * year

    # Adding a new temperature bias before the previous one is finished should fail.
    with pytest.raises(Exception) as e_info:
        glacier.add_temperature_bias(bias=2.5, duration=duration)

    # Progress a bit further
    year = 10
    glacier.progress_to_year(year)
    # We should have reached the final temp bias now.
    assert glacier.mass_balance.temp_bias == bias
    # This should've also have update the ELA, check against the original ELA.
    assert glacier.ela == real_mb.ela + 150 * 2
    assert glacier.age == 10
    # Progress even further, bias should not continue to evolve
    glacier.progress_to_year(20)
    assert glacier.mass_balance.temp_bias == bias
    assert glacier.ela == real_mb.ela + 150 * 2
    # If we then set a new bias this should start to evolve again.
    new_bias = -1.0
    new_duration = 10
    glacier.add_temperature_bias(bias=new_bias, duration=new_duration)
    # Progress
    year = 25
    glacier.progress_to_year(year)
    # What should the bias be now?
    # We should be going from the previous bias towards the new bias.
    assert glacier.mass_balance.temp_bias == bias + (
        (new_bias - bias) / new_duration * 5
    )

    # Progress further
    year = 35
    glacier.progress_to_year(year)
    assert glacier.mass_balance.temp_bias == new_bias
    assert glacier.ela == real_mb.ela + 150 * new_bias


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
