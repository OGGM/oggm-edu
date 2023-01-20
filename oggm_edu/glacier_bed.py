"""This module provides a class, GlacierBed, which aids the setup of a
glacier bed to use with the Glacier and SurgingGlacier classes.
"""

from oggm_edu.funcs import edu_plotter
from collections.abc import Sequence

# Other libraries.
import numpy as np
import pandas as pd
import warnings

# Plotting
from matplotlib import pyplot as plt


class GlacierBed:
    """The glacier bed used to construct a ``oggm_edu.Glacier``.


    Attributes
    ----------
    bed_h : array(float)
        Array of the bed surface heights. [m]
    bottom : int or float
        Bottom altitude of the glacier domain. [m]
    distance_along_glacier : array(float)
        Horisontal distance along the glacier bed. [km]
    map_dx :  int
        Grid resolution. [m]
    nx : int
        Number of gridpoints.
    top : int or float
        Top altitude of the glacier domain. [m]
    width : int or list(int)
        Width of the glacier (single scalar) or list of widths defining the
        width-profile of the glacier.
    widths : array(float)
        Interpolated widths along the distance of the glacier.
    """

    def __init__(
        self,
        top=None,
        bottom=None,
        width=None,
        altitudes=None,
        widths=None,
        slopes=None,
        slope_sections=None,
        nx=200,
        map_dx=100,
    ):
        """Initialise the bed. Pass single scalars for top, bottom and width
        to create a square glacier bed. For finer control of the width pass
        ``altitudes`` and ``widths`` as lists or tuples for custom geometry. This will linearly
        intepolate between the altitude/width pairs.

        To contol the slope of the glacier provide a single value to ``slopes``. For even finer contol
        pass a sequence of values to ``slopes`` along with a sequence of altitudes to ``slope_sections``.

        Parameters
        ----------
        top : int or float
            Elevation at the top of the bed domain in meters.
        bottom : int or float
            Elevation at the bottom of the bed domain in meters.
        width : int or float
            Width of the bed in meters. Generates a square bed.
        altitudes : array_like (ints or floats)
            list of values corresponding to the altitude/width distribution.
            First and last value will be the top and bottom.
            Length should match widths.
        widths : array_like, (ints of floats)
            List of values defining the widths along the glacier.
            Length should match altitudes.
        slopes : array_like(int)
            Define the slope of the bed, degrees. One or multiple values. For the latter,
            slope sections are required. Possible values range from -90 to 90 degrees.
            To create a hole, there has to be an increase in the altitude in slope_section.
        slope_sections : array_like(int)
            Defines the altitude spans for the slopes. Should start with the top altitude and
            end with the bottom altitude. The number of altitudes need to be one greater then
            the number of slopes.
        nx : int
            Number of grid points. Will be overriden if slope is provided.
        map_dx : int
            Grid point spacing in meters.
        """
        # Arg checks
        if (
            (top is None and altitudes is None)
            or (bottom is None and altitudes is None)
            or (top is not None and altitudes is not None)
            or (bottom is not None and altitudes is not None)
        ):
            raise ValueError("Provide either a top and bottom or altitudes.")

        if (width is None and widths is None) or (
            width is not None and widths is not None
        ):
            raise ValueError("Provide either a single width or a list of widths")
        if altitudes is not None and width is not None:
            raise ValueError("Not possible to combine altitude with width.")
        if top is not None and bottom is not None and widths is not None:
            raise ValueError("Not possible to combine widths with top and bottom.")

        # Check that width is a single scalar.
        if width is not None:
            # Ask for forgiveness...
            try:
                width + 1
            except TypeError:
                raise TypeError("Width should be single scalar (int/float)")

        # Geometry
        # If we have top and bottom.
        if top and bottom:
            self.top = top
            self.bottom = bottom
        # Else get it from the altitudes.
        else:
            self.top = altitudes[0]
            self.bottom = altitudes[-1]

        # Check the values of top and bottom.
        if self.top <= self.bottom or self.bottom < 0:
            raise ValueError(
                "Top of the bed has to be above the bottom."
                + " Bottom also has to be above 0"
            )
        # Set the resolution.
        if map_dx <= 10:
            msg = ("Setting the map resolution below 10 meters may lead to "
                  "very long runtimes.")
            warnings.warn(msg)
        self.map_dx = map_dx

        # Do we have a specified slope?
        self.slopes = None
        self.slope_sections = None
        if slopes:
            # If slopes is not a sequence, then make it one.
            if not isinstance(slopes, Sequence):
                slopes = [slopes]

            # Make sure that the provided slopes are reasonable.
            if (np.asarray(slopes) < -90).any() or (np.asarray(slopes) > 90).any():
                raise ValueError("Slopes should be above -85 and below 80 degrees.")
            #  Do we have sequence of both slopes and breakpoints?
            if isinstance(slopes, Sequence) and isinstance(slope_sections, Sequence):
                # Are they compatible?
                # There should be one more section compared to slopes
                if not len(slopes) == len(slope_sections) - 1:
                    raise ValueError(
                        "Number of slope sections should be one more then number of slopes"
                    )
                # Have to match top and bottom.
                elif slope_sections[0] != self.top or slope_sections[-1] != self.bottom:
                    raise ValueError(
                        "First and last value of slope_sections should match top and bottom."
                    )
            # If we passed a single slope, we can assign slope sections to still make use of our fancy algo.
            elif len(slopes) == 1:
                slope_sections = [self.top, self.bottom]

            # What is the height difference between the sections?
            slope_sections = np.asarray(slope_sections)
            slope_sections_diff = np.abs(np.diff(slope_sections))

            # How long does a segment has to be to have the correct slope angle?
            x_segments_length = slope_sections_diff / np.tan(np.deg2rad(slopes))
            # We add a zero to the start to begin the interpolation in the right place.
            # Take the cumsum to get the absolute position of each coord.
            x_segments_length = np.concatenate([[0], x_segments_length.cumsum()])

            # What does the total length of the glacier have to be?
            # This should be a float for correct interpolation.
            total_length = x_segments_length.max()
            # And how many gridpoints do we need for this?
            self.nx = int(total_length / self.map_dx)
            # Distance along the glacier: up to the total length in the closest number of grid points.
            self.distance_along_glacier = np.linspace(0, total_length, self.nx)
            # Interpolate the heights
            heights = np.interp(
                self.distance_along_glacier, x_segments_length, slope_sections
            )

            # We can now put the distance in kms
            self.distance_along_glacier = self.distance_along_glacier * 1e-3

            # Assign the heights.
            self.bed_h = heights

            # store readonly
            self.slopes = slopes
            self.slope_sections = slope_sections

        # Otherwise we just make a simple bed profile.
        else:
            self.nx = nx
            self.bed_h = np.linspace(self.top, self.bottom, self.nx)
            self.distance_along_glacier = (
                np.linspace(0, self.nx, self.nx) * map_dx * 1e-3
            )

        # Widths.
        # If width has a length of one, we have a constant width.
        if width:
            self.width = width
            self.widths = (np.zeros(self.nx) + self.width) / self.map_dx
        # If length of width and length of width altitudes are compatible,
        # we create a bed with variable width.
        elif len(altitudes) == len(widths):
            self.width = widths
            # First create a constant bed.
            tmp_w = np.zeros(self.nx)

            # Make sure we have lists.
            altitudes = list(altitudes)
            widths = list(widths)
            # Check that the provided altitudes make sense.
            altitudes_tmp = altitudes.copy()
            altitudes_tmp.sort(reverse=True)
            if not altitudes_tmp == altitudes:
                raise ValueError("Please provides altitudes in descending order.")
            # Loop over the altitude/width pairs and do a linear
            # interpolations between them.
            for i, alt in enumerate(altitudes[1:]):
                # We want to interpolate to the previos altitude step.
                inter_top = altitudes[i]
                # Select the values that we interpolate.
                mask = np.logical_and(self.bed_h <= inter_top, self.bed_h >= alt)
                # Linear interpolation between the widths.
                tmp_w[mask] = np.linspace(self.width[i], self.width[i + 1], mask.sum())
            # Assign the varied widths it.
            self.widths = tmp_w / self.map_dx

        # If noting works, raise an error.
        else:
            raise ValueError("Provided arguments are not compatible.")

    def __repr__(self):

        # Get the json representation of the object.
        json = self._to_json()

        # Create a nicer string of it.
        string = "Glacier bed \n"
        for key, value in json.items():
            string += f"{key}: {value} \n"
        return string

    def _repr_html_(self):
        """HTML representations"""
        # Get attris
        attrs = self._to_json()
        df = pd.DataFrame.from_dict(attrs, orient="index")
        df.columns = [""]
        df.index.name = type(self).__name__

        return df._repr_html_()

    def _to_json(self):
        """Json representation of the bed"""
        # Is the bed width constant or variable?
        w_string = "constant" if type(self.width) in (int, float) else "variable"
        # Create a dictionary with some of the attributes.
        json = {
            "Bed type": f"Linear bed with a {w_string} width",
            "Top [m]": self.top,
            "Bottom [m]": self.bottom,
            "Width(s) [m]": [self.width],
            "Length [km]": self.distance_along_glacier[-1],
        }
        return json

    def _decide_xlim(self):
        return 0, self.distance_along_glacier[-1] * 1.02

    def _create_base_plot(self, axes=None, title=None):
        """Create the base plot the glacier bed"""

        if axes is not None:
            fig = plt.gcf()
            ax1, ax2 = axes
        else:
            fig, (ax1, ax2) = plt.subplots(
                nrows=2, gridspec_kw={"height_ratios": [2, 1]}, sharex=True
            )

        # Plot the bed
        ax1.plot(
            self.distance_along_glacier,
            self.bed_h,
            label="Bedrock",
            ls=":",
            c="k",
            lw=2,
            zorder=3,
        )
        # And fill it.
        ax1.fill_between(self.distance_along_glacier, -100, self.bed_h,
                         color="lightgrey")
        # Some labels etc.
        ax1.set_ylabel("Altitude [m]")
        ax1.set_facecolor("#ADD8E6")
        ax1.set_ylim(self.bottom, self.top + 400)

        # Fill the bed.
        ax2.fill_between(
            self.distance_along_glacier,
            -self.widths / 2 * self.map_dx,
            self.widths / 2 * self.map_dx,
            color="lightgrey",
        )
        # More styling.
        ax2.set_facecolor("darkgrey")
        ax2.axhline(0, c="k")
        # We add 2% of the bed length to the plot to have some space.
        ax2.set_xlim(self._decide_xlim())
        ax2.set_xlabel("Distance along glacier [km]")
        ax2.set_ylabel("Width [m]")
        if title is None:
            ax1.set_title("Glacier domain")
        else:
            ax1.set_title(title)
        ax1.legend()

        return fig, ax1, ax2

    @edu_plotter
    def plot(self):
        """Plot the bed"""
        # Since we are not modifying the base here, we don't need to assign
        # any of the returns.
        self._create_base_plot()
