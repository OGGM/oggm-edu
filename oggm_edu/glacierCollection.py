'''This module provides a utility class, GlacierCollection, designed to ease
the handling of multiple glaciers.
'''

# Internals
from oggm_edu.glacier import Glacier

# Other libraries.
import seaborn as sns
import pandas as pd
import collections

# Plotting
from matplotlib import pyplot as plt

# Plotting
sns.set_context('notebook')
sns.set_style('ticks')
plt.rcParams['figure.figsize'] = (12, 9)


class GlacierCollection:
    '''This is class for storing multiple glaciers, providing convenient
    methods for comparing them.
    '''

    def __init__(self, glacier_list=None):
        '''Initialise the glacier collection.

        Parameters
        ----------
        glacier_list: list of glaciers objects
            Defaults to none. Has the possibility to add glaciers on the go.
        '''

        self._glaciers = []

        # Do we have a list of glaciers?
        if glacier_list:
            # Check that all are Glaciers.
            if all(isinstance(glacier, Glacier) for glacier in glacier_list):
                self._glaciers = glacier_list

    def __repr__(self):
        return f'Glacier collection with {len(self._glaciers)} glaciers.'

    def _repr_html_(self):
        # Pretty representation for notebooks.
        # Get the first glacier and base the creation of the dataframe of this.
        # If we have glaciers in the collection.
        if len(self._glaciers) > 0:
            json = {**self._glaciers[0]._to_json(),
                    **self._glaciers[0].bed._to_json(),
                    **self._glaciers[0].mass_balance._to_json()
                    }
            # Create the dataframe.
            df = pd.DataFrame(json, index=[0])
            # We then loop over the rest of the collection.
            for glacier in self._glaciers[1:]:
                # Next json representation
                json = {**glacier._to_json(), **glacier.bed._to_json(),
                        **glacier.mass_balance._to_json()}
                # Add it to the df.
                df = df.append(json, ignore_index=True)
                df.index.name = "Glacier"
            # Return the html representation of the dataframe.
            return df._repr_html_()
        # If empty.
        else:
            pass

    def check_collection(self, glacier):
        '''Utility method. Check if the glaciers obey the collection rules.
        They need to have the same domains for this to make sense I think.'''
        # TODO

    @property
    def glaciers(self):
        return self._glaciers

    def add(self, glacier):
        '''Add a glacier to the collection.

        Parameters
        ----------
        glacier: oggm.edu Glacier object or array_like with
        Glacier objects
        '''
        # Check if iterable
        if isinstance(glacier, collections.Sequence):
            for glacier in glacier:
                # Check that glacier is of the right type.
                if not isinstance(glacier, Glacier):
                    raise TypeError('Glacier collection can only'
                                    ' contain glacier objects.')
                # Is the glacier already in the collection?
                if glacier in self._glaciers:
                    raise AttributeError('Glacier is already in collection')
                # If the glacier is an instance of Glacier, we can add it to
                # the collection.
                else:
                    self._glaciers.append(glacier)
        # If not iterable
        else:
            # Check that glacier is of the right type.
            if not isinstance(glacier, Glacier):
                raise TypeError('Glacier collection can only'
                                ' contain glacier objects.')
            # Is the glacier already in the collection?
            if glacier in self._glaciers:
                raise AttributeError('Glacier is already in collection')
            # If the glacier is an instance of Glacier, we can add it to
            # the collection.
            else:
                self._glaciers.append(glacier)

    def progress_to_year(self, year):
        '''Progress the glaciers within the collection to
        the specified year.

        Parameters
        ----------
        year: int
            Which year to grow the glaciers.
        '''
        if len(self._glaciers) < 1:
            raise ValueError('Collection is empty')

        # Loop over the glaciers within the collection.
        for glacier in self._glaciers:
            glacier.progress_to_year(year)

    def progress_to_equilibrium(self):
        '''Progress the glaciers within the collection to equilibrium.
        '''
        if len(self._glaciers) < 1:
            raise ValueError('Collection is empty')

        # Loop.
        for glacier in self._glaciers:
            glacier.progress_to_equilibrium()

    def plot(self):
        '''Plot the glaciers in the collection to compare them.'''

        if len(self._glaciers) < 1:
            raise ValueError('Collection is empty')
        # We use this to plot the bedrock etc.
        gl1 = self._glaciers[0]
        # Get the ax from the first plot
        fig, ax = plt.subplots()
        # Bedrock
        ax.plot(gl1.bed.distance_along_glacier, gl1.bed.bed_h, label='Bedrock',
                ls=':', c='k', lw=2, zorder=3)
        ax.set_ylim((gl1.bed.bottom, gl1.bed.top + 200))
        # Fill it in.
        ax.fill_betweenx(gl1.bed.bed_h, gl1.bed.distance_along_glacier,
                         facecolor='lightgrey')

        # Set the title.
        ax.set_title('Glacier collection')

        elas = []
        # Loop over the collection.
        for i, glacier in enumerate(self._glaciers):
            # Plot the surface
            if glacier.current_state is not None:
                # Masking shenanigans.
                diff = glacier.current_state.surface_h - glacier.bed.bed_h
                mask = diff > 0
                idx = diff.argmin()
                mask[:idx+1] = True
                # Fill the ice.
                ax.fill_between(glacier.bed.distance_along_glacier,
                                glacier.current_state.surface_h,
                                glacier.bed.bed_h,
                                where=mask,
                                facecolors='white',
                                # edgecolors=color_cycler(i),
                                # lw=2,
                                )
                # Plot outline
                ax.plot(glacier.bed.distance_along_glacier[mask],
                        glacier.current_state.surface_h[mask],
                        label=f'Glacier nr. {i+1} at year'
                        + f' {glacier.age}')
                # Ylim
                ax.set_ylim((gl1.bed.bottom,
                             gl1.current_state.surface_h[0]+200))
            elas.append(glacier.ELA)

        # Loop the unique ELAs.
        for i, ela in enumerate(set(elas)):
            # Plot the ELA
            ax.axhline(ela, ls='--', zorder=1)
            # Label if elas are equal.
            if len(set(elas)) == 1:
                ax.text(glacier.bed.distance_along_glacier[-1], ela + 10,
                        'ELAs are equal', ha='right', va='bottom')
            # If we have multiple ELAs.
            else:
                ax.text(glacier.bed.distance_along_glacier[-1], ela + 10,
                        f'ELA  nr {i+1}', ha='right', va='bottom')

        # axis labels.
        ax.set_xlabel('Distance along glacer [km]')
        ax.set_ylabel('Altitude [m]')
        ax.set_xlim((0, gl1.bed.distance_along_glacier[-1]+2))
        ax.set_facecolor('#ADD8E6')
        plt.legend(loc='lower left')
        # Add a second legend with infos.
        # It would be cool to only show attributes that are different.
        labels = []
        for glacier in self._glaciers:
            # Create the label
            label = f'ELA: {glacier.ELA} \n' \
                f'MB grad: {glacier.mb_gradient} \n' \
                f'Age: {glacier.age} \n' \
                f'Creep: {glacier.creep:.2e} \n' \
                f'Sliding: {glacier.basal_sliding}'
            # Append the label to the list.
            labels.append(label)
        # Get the handles back
        handles, _ = ax.get_legend_handles_labels()
        # Create the legend
        fig.legend(handles[1:], labels, title='Glacier info',
                   loc='upper left', bbox_to_anchor=(0.9, 0.89))

    def plot_history(self):
        '''Plot the histories of the collection'''

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

        for glacier in self._glaciers:
            # Plot the length.
            glacier.history.length_m.plot(ax=ax1)
            # Plot the volume
            glacier.history.volume_m3.plot(ax=ax2)
            # Plot the area
            glacier.history.area_m2.plot(ax=ax3,
                                         label=f'ELA: {glacier.ELA} \n' +
                                         f'MB grad: {glacier.mb_gradient} \n' +
                                         f'Age: {glacier.age} \n' +
                                         f'Creep: {glacier.creep:.2e} \n' +
                                         f'Sliding: {glacier.basal_sliding}')
        # Decorations
        ax1.set_xlabel('')
        ax1.set_title('Glacier collection evolution')
        ax1.annotate('Glacier length', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax1.set_ylabel('Length [m]')
        ax2.set_xlabel('')
        ax2.annotate('Glacier volume', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax2.set_ylabel('Volume [m$^3$]')
        ax3.set_xlabel('Year')
        ax3.annotate('Glacier area', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax3.set_ylabel('Area [m$^2$]')
        handels, labels = ax3.get_legend_handles_labels()
        fig.legend(handels, labels, loc='upper left', ncol=1,
                   title='Glacier info',
                   bbox_to_anchor=(0.9, 0.89))
