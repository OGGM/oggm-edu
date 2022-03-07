from oggm_edu import GlacierBed
from numpy.testing import assert_equal
import numpy as np
import pytest


def test_constructor_logic():
    """Test the constructor logic"""

    # Test some cases where constructor should raise.
    # Multiple widhts without altitudes.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(top=3400, bottom=1000, widths=[500, 400])
    # Altitudes with single width
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(altitudes=[2000, 1500], width=500)

    # We dont pass top/bottom along with altitudes.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(top=3400, bottom=1000, altitudes=[2000, 1500], widths=[500, 300])
    # Width and widths
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(top=3400, bottom=1000, width=200, widths=[500, 300])
    # Test top/bottom logic.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(top=2400, bottom=3000, width=500)
    # Same but with altitudes. Kind of redundat because of the ascending check that is done.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(altitudes=[2000, 1900, 2100], widths=[500, 400, 200])
    # Altitudes should be in ascending order.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(altitudes=[3000, 2200, 2500, 1800], widths=[500, 500, 400, 200])


def test_constructor_attribute_assignment():
    """Test that check what happens if inis logic passes."""

    bed = GlacierBed(top=3400, bottom=1000, width=500)
    assert bed.top == 3400
    assert bed.bottom == 1000

    bed = GlacierBed(altitudes=[3600, 2000, 1500], widths=[500, 300, 200])
    assert bed.top == 3600
    assert bed.bottom == 1500

    # Check widths, use very few gridpoints, easier to compute manually.
    bed = GlacierBed(altitudes=[2500, 2000, 1500], widths=[500, 500, 250], nx=5)
    # Should be 250 m increments.
    assert_equal(bed.bed_h, [2500, 2250, 2000, 1750, 1500])
    # What should the widhts be? Linearly interpolated.
    assert_equal(bed.widths * bed.map_dx, [500, 500, 500, 375, 250])


def test_non_linear_bed_constructor():
    """Testing init of non-linear bed profiles."""
    # Should throw when we don't have enough breakpoints.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(
            altitudes=[2500, 2000, 1500],
            widths=[500, 500, 250],
            slopes=[25, 15],
            slope_sections=[2500, 2200],
        )

    # Should throw since bottom and last slope breakpoint don't match.
    with pytest.raises(Exception) as e_info:
        _ = GlacierBed(
            altitudes=[2500, 2000, 1500],
            widths=[500, 500, 250],
            slopes=[25, 15],
            slope_sections=[2500, 2200, 1400],
        )

    # 45 degrees beds are easy. Just linspace.
    bed = GlacierBed(top=3600, bottom=3000, width=300, slopes=[45])

    # Easy correct bed.
    bed_h_corr = np.linspace(3600, 3000, 6)
    # They should correspond.
    assert_equal(bed_h_corr, bed.bed_h)

    # This test should maybe work, but I'm also not sure if it is possible to get to work.
    # Would require the distance_along_glacier to be variable.
    # Basically the section that is supposed to be 45 degrees is just close to 45 degrees.
    # This is because the interpolation over the distance_along_glacier does not take the
    # exact step size needed for 45 degrees.
    # bed = GlacierBed(
    #     top=3600,
    #     bottom=2000,
    #     width=300,
    #     slopes=[45, 10],
    #     slope_breakpoints=[3600, 3000, 2000],
    # )

    # assert_equal(bed_h_corr, bed.bed_h[:6])

    # # Easy correct bed.
    # bed_h_corr = np.linspace(3600, 3000, 6)
    # # They should correspond.
    # assert_equal(bed_h_corr, bed.bed_h)

    bed = GlacierBed(top=3600, bottom=3000, width=300, slopes=[44])
    # Bed top and bottom should always equal the first and last value in the bed_h.
    assert bed.bed_h[0] == bed.top
    assert bed.bed_h[-1] == bed.bottom

    # A more complex bed.
    bed = GlacierBed(
        altitudes=[2500, 2000, 1500],
        widths=[500, 500, 250],
        slopes=[25, 15],
        slope_sections=[2500, 2200, 1500],
    )
    # Bed top and bottom should always equal the first and last value in the bed_h.
    assert bed.bed_h[0] == bed.top
    assert bed.bed_h[-1] == bed.bottom
