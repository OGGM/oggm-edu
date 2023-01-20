import matplotlib.pyplot as plt

from oggm_edu import GlacierBed, Glacier, MassBalance, GlacierCollection
import pytest

mb = MassBalance(ela=3000, gradient=8)
bed = GlacierBed(top=3700, bottom=1500, width=600)
glacier1 = Glacier(bed=bed, mass_balance=mb)
glacier2 = Glacier(bed=bed, mass_balance=mb)
bed_new = GlacierBed(top=3700, bottom=2500, width=300, slopes=45)
glacier3 = Glacier(bed=bed_new, mass_balance=mb)

# We need a global collection for testing the plots, for some efficiency.
collection = GlacierCollection()
collection.fill(glacier1, 2)
collection.change_attributes(attributes_to_change={"gradient": [10, 15]})
year = 200
collection.progress_to_year(year)


def test_constructor():
    """Can we initialise a collection from a list directly?"""
    collection = GlacierCollection([glacier1, glacier2])

    # Should have length 2.
    assert len(collection.glaciers) == 2
    assert collection.summary().loc[1].Age == 0


def test_check_collection():
    """Check if the glaciers in the collection are the same."""

    # Check collection should be true since glaciers have the same beds.
    collection = GlacierCollection([glacier1, glacier2])
    print(collection._check_collection())
    assert collection._check_collection()

    # Check collection should be false. Glaciers have different beds.
    collection = GlacierCollection([glacier1, glacier3])
    assert not collection._check_collection()

    # Check that plot throws when we have different beds.
    with pytest.raises(Exception) as e_info:
        collection.plot()


def test_add():
    collection = GlacierCollection([glacier1, glacier2])
    # We can add a new glacier
    collection.add(glacier1.copy())
    # Did we add a glacier?
    assert len(collection.glaciers) == 3

    # But not possible to add the same glacier again.
    with pytest.raises(Exception) as e_info:
        collection.add(glacier1)


def test_fill():
    collection = GlacierCollection()

    # Fill it.
    collection.fill(glacier1, 3)
    assert len(collection.glaciers) == 3


def test_change_attributes():
    """Test the change_attributes method."""
    # We need a collection.
    collection = GlacierCollection()
    collection.fill(glacier1, 2)
    # First check that attrbites are what we think.
    assert collection.glaciers[0].mass_balance.gradient == 8
    assert collection.glaciers[1].mass_balance.gradient == 8

    # Then lets change the creep.
    collection.change_attributes(attributes_to_change={"creep": [10, 15]})
    # Did it work?
    assert collection.glaciers[0].creep == 10
    assert collection.glaciers[1].creep == 15

    # Did shouldn't work, check that it raises. False attribute.
    with pytest.raises(Exception) as e_info:
        collection.change_attributes(attributes_to_change={"gradients": [10, 15]})
    # Wrong length of provided values
    with pytest.raises(Exception) as e_info:
        collection.change_attributes(attributes_to_change={"gradient": [10, 15, 5]})
    # Completetly wrong attribute
    with pytest.raises(Exception) as e_info:
        collection.change_attributes(attributes_to_change={"year": [10, 15]})

    # Change another attribute.
    collection.change_attributes(attributes_to_change={"gradient": [10, 15]})
    # Did it work?
    assert collection.glaciers[0].mass_balance.gradient == 10
    assert collection.glaciers[1].mass_balance.gradient == 15

    # This should also work
    collection = GlacierCollection([glacier1, glacier2])
    # Change another attribute.
    collection.change_attributes(attributes_to_change={"gradient": [10, 15]})
    # Did it work?
    assert collection.glaciers[0].mass_balance.gradient == 10
    assert collection.glaciers[1].mass_balance.gradient == 15

    # Testing the expression assignment mechanism
    collection = GlacierCollection()
    collection.fill(glacier1, n=5)
    # Change another attribute.
    collection.change_attributes(
        attributes_to_change={"basal_sliding": [10, 10, 10, 10, 10]}
    )
    collection.change_attributes(
        attributes_to_change={"basal_sliding": ["* 5", "/ 5", "+ 5", "- 5", ""]}
    )
    # Did it work?
    assert collection.glaciers[0].basal_sliding == 50
    assert collection.glaciers[1].basal_sliding == 2
    assert collection.glaciers[2].basal_sliding == 15
    assert collection.glaciers[3].basal_sliding == 5
    assert collection.glaciers[4].basal_sliding == 10


def test_progress_to_year():
    """Test progressing the collection to a specified year"""
    mb = MassBalance(ela=3000, gradient=8)
    bed = GlacierBed(top=3700, bottom=1500, width=600)
    glacier1 = Glacier(bed=bed, mass_balance=mb)
    glacier2 = Glacier(bed=bed, mass_balance=mb)
    collection = GlacierCollection([glacier1, glacier2])
    collection = GlacierCollection([glacier1, glacier2])
    # Essntially all glaciers in the collection should be of the same age.

    year = 100
    collection.progress_to_year(year)

    # Check the ages.
    assert collection.glaciers[0].age == year
    assert collection.glaciers[1].age == year

    # Empty collection should raise.
    collection = GlacierCollection()
    with pytest.raises(Exception) as e_info:
        collection.progress_to_year(year)


def test_progress_to_equilibrium():
    """Test progressing a collection of glaciers to equilibrium."""
    mb = MassBalance(ela=3000, gradient=8)
    bed = GlacierBed(top=3700, bottom=1500, width=600)
    glacier1 = Glacier(bed=bed, mass_balance=mb)
    glacier2 = Glacier(bed=bed, mass_balance=mb)
    collection = GlacierCollection([glacier1, glacier2])

    # Since the glaciers in the collection have the same attributes, they should
    # reach the same equilibrium state.

    collection.progress_to_equilibrium()
    assert collection.glaciers[0].age == collection.glaciers[1].age


def test_plot_side_by_side():
    mb = MassBalance(ela=3000, gradient=8)
    bed1 = GlacierBed(top=3700, bottom=1500, width=600)
    bed2 = GlacierBed(top=3700, bottom=2300, width=600)
    bed3 = GlacierBed(top=3700, bottom=2900, width=600)
    glacier1 = Glacier(bed=bed1, mass_balance=mb)
    glacier2 = Glacier(bed=bed2, mass_balance=mb)
    glacier3 = Glacier(bed=bed3, mass_balance=mb)
    collection = GlacierCollection([glacier1, glacier2, glacier3][::-1])
    collection.progress_to_year(10)
    collection.plot_side_by_side(figsize=(12, 5))
