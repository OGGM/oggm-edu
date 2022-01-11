'''This module provides a class, GlacierBed, which aids the setup of a
glacier bed to use with the Glacier and SurgingGlacier classes.
'''

# Other libraries.
import numpy as np
import seaborn as sns
import pandas as pd

# Plotting
from matplotlib import pyplot as plt
# Import OGGM things.

# Plotting
sns.set_context('notebook')
sns.set_style('ticks')
plt.rcParams['figure.figsize'] = (12, 9)


class GlacierBed:
    '''The glacier bed'''

    def __init__(self, top=None, bottom=None, width=None, altitudes=None,
                 widths=None, slope=None, nx=200, map_dx=100):
        '''Initialise the bed. Pass single scalars for top, bottom and width
         to create a square glacier bed. For finer control pass altitudes and
         widths as lists or tuples for custom geometry. Will linearly
         intepolate between the altitude/width pairs.

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
        slope : float
            Define the slope of the bed, decimal
        nx : int
            Number of grid points.
        map_dx : int
            Grid point spacing in meters.
        '''
        # Arg checks
        if (top is None and altitudes is None) or \
                (bottom is None and altitudes is None) or \
                (top is not None and altitudes is not None) or \
                (bottom is not None and altitudes is not None):
            raise ValueError('Provide either a top and bottom or altitudes.')

        if (width is None and widths is None) or \
                (width is not None and widths is not None):
            raise ValueError('Provide either a single width'
                             ' or a list of widths')
        if (altitudes is not None and width is not None):
            raise ValueError('Not possible to combine altitude with width.')
        if (top is not None and bottom is not None and widths is not None):
            raise ValueError('Not possible to combine widths '
                             'with top and bottom.')

        # Check that width is a single scalar.
        if width is not None:
            # Ask for forgiveness...
            try:
                width + 1
            except TypeError:
                raise TypeError('Width should be single scalar (int/float)')

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
        if self.top <= self.bottom and self.bottom < 0:
            raise ValueError('Top of the bed has to be above the bottom.' +
                             ' Bottom also has to be above 0')
        # Calculate the slope correction
        if slope:
            if slope >= 1. or slope <= 0.:
                raise ValueError('Slope shoud be between 0 and 1 (not equal)')
            # If there is a slop we re calculate the map_dx
            else:
                map_dx = (self.top - self.bottom) / (nx * slope)

        # Set the resolution.
        self.map_dx = map_dx
        # Initialise the bed
        self.bed_h = np.linspace(self.top, self.bottom, nx)
        self.distance_along_glacier = np.linspace(0, nx, nx) *\
            self.map_dx * 1e-3
        # Widths.
        # If width has a length of one, we have a constant width.
        if width:
            self.width = width
            self.widths = (np.zeros(nx) + self.width) / map_dx
        # If length of width and length of width altitudes are compatible,
        # we create a bed with variable width.
        elif len(altitudes) == len(widths):
            self.width = widths
            # First create a constant bed.
            tmp_w = np.zeros(nx)

            # Make sure we have lists.
            altitudes = list(altitudes)
            widths = list(widths)
            # Check that the provided altitudes make sense.
            altitudes_tmp = altitudes.copy()
            altitudes_tmp.sort(reverse=True)
            if not altitudes_tmp == altitudes:
                raise ValueError('Please provides altitudes'
                                 ' in descending order.')
            # Loop over the altitude/width pairs and do a linear
            # interpolations between them.
            for i, alt in enumerate(altitudes[1:]):
                # We want to interpolate to the previos altitude step.
                inter_top = altitudes[i]
                # Select the values that we interpolate.
                mask = np.logical_and(self.bed_h <= inter_top,
                                      self.bed_h >= alt)
                # Linear interpolation between the widths.
                tmp_w[mask] = np.linspace(self.width[i], self.width[i+1],
                                          mask.sum())
            # Assign the varied widths it.
            self.widths = tmp_w / map_dx

        # If noting works, raise an error.
        else:
            raise ValueError('Provided arguments are not compatible.')

    def __repr__(self):

        # Get the json representation of the object.
        json = self._to_json()

        # Create a nicer string of it.
        string = 'Glacier bed \n'
        for key, value in json.items():
            string += f'{key}: {value} \n'
        return string

    def _repr_html_(self):
        '''HTML representations'''
        # Get attris
        attrs = self._to_json()
        df = pd.DataFrame.from_dict(attrs, orient="index")
        df.columns = [""]
        df.index.name = type(self).__name__

        return df._repr_html_()

    def _to_json(self):
        '''Json representation of the bed'''
        # Is the bed width constant or variable?
        w_string = ('constant' if type(self.width) in (int, float)
                    else 'variable')
        # Create a dictionary with some of the attributes.
        json = {
            'Bed type': f'Linear bed with a {w_string} width',
            'Top [m]': self.top,
            'Bottom [m]': self.bottom,
            'Width(s) [m]': [self.width],
            'Length [km]': self.distance_along_glacier[-1]
        }
        return json

    def plot(self):
        '''Plot the glacier bed'''

        fig, (ax1, ax2) = plt.subplots(nrows=2,
                                       gridspec_kw={'height_ratios': [2, 1]},
                                       sharex=True)

        # Plot the bed
        ax1.plot(self.distance_along_glacier, self.bed_h, label='Bedrock',
                 ls=':', c='k', lw=2, zorder=3)
        # And fill it.
        ax1.fill_betweenx(self.bed_h, self.distance_along_glacier,
                          color='lightgrey')
        # Some labels etc.
        ax1.set_ylabel('Altitude [m]')
        ax1.set_facecolor('#ADD8E6')
        ax1.set_ylim(self.bottom, self.top + 400)

        # Fill the bed.
        ax2.fill_between(self.distance_along_glacier,
                         -self.widths/2 * self.map_dx,
                         self.widths/2 * self.map_dx,
                         color='lightgrey')
        # More styling.
        ax2.set_facecolor('darkgrey')
        ax2.axhline(0, c='k')
        plt.xlim((0, self.distance_along_glacier[-1] + 2))
        plt.xlabel('Distance along glacier [km]')
        plt.ylabel('Distance from centerline [m]')
        ax1.set_title('Glacier domain')
        ax1.legend()
