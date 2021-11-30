'''This class provides a high level interface to the OGGM modelling framwork,
suitable for purely educational purposes, understanding the basics of
glacier mechanics.
'''

# Other libraries.
import numpy as np
import seaborn as sns
import xarray as xr
import warnings

# Plotting
from matplotlib import pyplot as plt
# Import OGGM things.
from oggm.core.flowline import FluxBasedModel, RectangularBedFlowline
from oggm.core.massbalance import LinearMassBalance

from oggm import cfg
# Initialise cfg
cfg.initialize_minimal()
sns.set_context('notebook')
sns.set_style('ticks')
plt.rcParams['figure.figsize'] = (10, 9)


class GlacierBed:
    '''The glacier bed'''

    def __init__(self, top=None, bottom=None, width=None, altitudes=None,
                 widths=None, nx=200, map_dx=100):
        '''Initialise the bed. Pass single scalars for top, bottom and width
         to create a square glacier bed. For finer control pass altitudes and
         widths as lists or tuples for custom geometry. Will linearly
         intepolate between the altitude/width pairs.

        Parameters
        ----------
        top : int/float
            Elevation at the top of the bed domain in meters.
        bottom : int/float
            Elevation at the bottom of the bed domain in meters.
        width : int/float
            Width of the bed in meters. Generates a square bed.
        altitudes : int/float, list/tuple
            list of values corresponding to the altitude/width distribution.
            First and last value will be the top and bottom.
            Length should match widths.
        widths : int/float, list/tuple
            List of values defining the widths along the glacier.
            Length should match altitudes.
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
        self.map_dx = map_dx
        # Initialise the bed
        self.bed_h = np.linspace(self.top, self.bottom, nx)
        self.distance_along_glacier = np.linspace(0, nx, nx) * map_dx * 1e-3
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

            altitudes = list(altitudes)
            widths = list(widths)
            # Check that altitudes make sense.
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
            raise ValueError('Width and altitude widths are not compatible.')

    def __repr__(self):
        w_string = ('constant' if type(self.width) in (int, float)
                    else 'variable')
        string = f'Linear glacier bed with a {w_string} width.' \
                 f'\n Top: {self.top} m.' \
                 f'\n Bottom: {self.bottom} m.' \
                 f'\n Widths: {self.width}'
        return string

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
        ax1.set_ylabel('Altitude [m]')
        ax1.set_facecolor('#ADD8E6')
        ax1.set_ylim(self.bottom, self.top + 400)
        # Fill the bed.
        ax2.fill_between(self.distance_along_glacier,
                         -self.widths/2 * self.map_dx,
                         self.widths/2 * self.map_dx,
                         color='lightgrey')
        ax2.set_facecolor('darkgrey')
        ax2.axhline(0, c='k')
        plt.xlim((0, self.distance_along_glacier[-1] + 2))
        plt.xlabel('Distance along glacier [km]')
        plt.ylabel('Distance from centerline [m]')
        ax1.set_title('Glacier domain')
        ax1.legend()


class Glacier:
    '''The glacier object'''

    def __init__(self, bed):
        '''Initialise a glacier.

        Parameters
        ----------
        bed : bed object

        '''
        # Check the type of the bed.
        if not isinstance(bed, GlacierBed):
            raise TypeError('The bed has to be of the type GlacierBed.')
        # Save the bed.
        self.bed = bed
        # Set the surface height.
        self.surface_h = self.bed.bed_h

        # Mass balance
        self._ELA = None
        self._mb_gradient = None
        self._mb_model = None

        # Initilaise the flowline
        self.initial_state = self.init_flowline()
        self.current_state = None
        self.model_state = None

        # Descriptives
        # Store the age of the glacier outside the model object.
        self._age = 0.
        # This is used to store the history of the glacier evolution.
        self._history = None

    def __repr__(self):
        '''Pretty representation of the glacier object'''

        # Do we have a current state?
        state = self.state()
        string = f'Glacier at year {int(self.age)}' \
                 + f'\nELA: {self.ELA}' \
                 + f'\nLength {state.length_m} m.' \
                 + f'\nArea {state.area_km2:.3f} km2.\nVolume' \
                 + f' {state.volume_km3:.3f} km3' \
                 + f'\n{self.bed}'
        return string

    def init_flowline(self):
        return RectangularBedFlowline(surface_h=self.surface_h,
                                      bed_h=self.bed.bed_h,
                                      widths=self.bed.widths,
                                      map_dx=self.bed.map_dx)

    @property
    def ELA(self):
        return self._ELA

    @ELA.setter
    def ELA(self, value):
        '''Define the equilibrium line altitude.

        Parameters
        ----------
        value : float
            Altitude of the ELA.
        '''
        # We cant have a negative ELA.
        if value < 0:
            raise ValueError('ELA below 0 not allowed.')

        self._ELA = value
        # If we have the gradient, set the mb_model
        if self.mb_gradient:
            self._mb_model = LinearMassBalance(self.ELA, grad=self.mb_gradient)

    @property
    def mb_gradient(self):
        return self._mb_gradient

    @mb_gradient.setter
    def mb_gradient(self, value):
        '''Define the mass balance gradient.

        Parameters
        ----------
        value : float
            Mass balance altitude gradient, mm/m.
        '''
        # We cant have a negative gradient.
        if value < 0:
            raise ValueError('Mass balance gradient less than 0 not allowed')

        self._mb_gradient = value
        # If we have the ELA, set the mb_model
        if self.ELA:
            self._mb_model = LinearMassBalance(self.ELA, grad=self.mb_gradient)

    @property
    def mb_model(self):
        return self._mb_model

    def annual_mass_balance(self):
        return self.mb_model.get_annual_mb(self.surface_h) * cfg.SEC_IN_YEAR

    def state(self):
        state = self.initial_state
        # If we have a current state
        if self.current_state:
            state = self.current_state
        return state

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        'Set the age of the age of the glacier.'
        self._age = value

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, obj):
        'Set the glacier history object'
        if self._history is None:
            self._history = obj
        else:
            self._history = xr.combine_by_coords([self.history, obj],
                                                 combine_attrs='override')

    def progress_to_year(self, year):
        '''Method to progress the glacier to year n.

        Parameters
        ----------
        year : int
            Year until which to progress the glacier.
        '''
        # Check if the glacier has a masss balance model
        if not self.mb_model:
            string = 'To evolve the glacier it needs a mass balance.' \
                      + '\nMake sure the ELA and mass balance gradient' \
                      + ' are defined.'
            raise NotImplementedError(string)

        elif year < 0:
            raise ValueError('Year has to be above zero')

        elif year <= self.age:
            warnings.warn('Year has to be above the current age of'
                          + ' the glacier. It is not possible to'
                          + ' de-age the glacier.'
                          + ' Geometry will remain.')

        else:
            # Check if we have a current state already.
            state = self.state()
            # Initialise the model
            model = FluxBasedModel(state, mb_model=self.mb_model, y0=self.age)
            # Run the model.
            try:
                self.history = model.run_until_and_store(year)
            except RuntimeError:
                print('Glacier outgrew its domain and had to stop.')
                # raise RuntimeError('Glacier grew outside its domain.'
                #                    + ' Try raising the ELA.')

            self.current_state = model.fls[0]
            self.model_state = model
            self.age = model.yr

    def progress_to_equilibrium(self, years=2500):
        'Method to grow the glacier to equilibrium.'

        def stop_function(model, previous_state):
            '''Function to stop the simulation when equilbrium is
            reached. Basically a re-shape of the criterium of
            run_until_equilibrium.'''
            # We don't stop unless
            stop = False
            # Ambigous rate
            rate = 0.001
            max_ite = 500
            # If we have a previous step check it
            if previous_state is not None:
                # Here we save some stuff to diagnose the eq. state
                # If this is true, we update the state:
                if ((previous_state['t_rate'] > rate) and
                        (previous_state['ite'] <= max_ite) and
                        (previous_state['was_close_zero'] < 5)):

                    # Increase iterations.
                    previous_state['ite'] += 1
                    # Get the current volume
                    v_af = model.volume_m3
                    # If volume before is close to zero, update counter.
                    if np.isclose(previous_state['v_bef'], 0, atol=1):
                        previous_state['was_close_zero'] += 1
                        previous_state['t_rate'] = 1
                    # If not close to zero, update how slow volume is updating.
                    else:
                        previous_state['t_rate'] =\
                            (np.abs(v_af - previous_state['v_bef'])
                                / previous_state['v_bef'])
                    previous_state['v_bef'] = v_af
                # If we go over the iteration limit.
                elif previous_state['ite'] > max_ite:
                    raise RuntimeError('Not able to find equilbrium')
                # Otherwise we stop.
                else:
                    stop = True

            # If we don't have a previous state, define it.
            else:
                previous_state = {'ite': 0, 'was_close_zero': 0,
                                  't_rate': 1,
                                  'v_bef': model.volume_m3}

            return stop, previous_state

        # Check if the glacier has a masss balance model
        if not self.mb_model:
            string = 'To grow the glacier it needs a mass balance.' \
                      + '\nMake sure the ELA and mass balance gradient' \
                      + ' are defined.'
            raise NotImplementedError(string)

        else:
            state = self.state()
            # Initialise the model
            model = FluxBasedModel(state, mb_model=self.mb_model, y0=self.age)
            # Run the model.
            try:
                #  Run with a stopping criteria.
                out = model.run_until_and_store(years,
                                                stop_criterion=stop_function)
                # We need to drop the nan years
                out = out.dropna(dim='time')
                # Add the history dataset.
                self.history = out

            except RuntimeError:
                print('Glacier grew out of its domain and had to stop.')

            self.current_state = model.fls[0]
            self.age = model.yr
            self.model_state = model

    def plot(self):
        '''Plot the glacier'''
        fig, (ax1, ax2) = plt.subplots(nrows=2,
                                       gridspec_kw={'height_ratios': [2, 1]},
                                       sharex=True)

        # Plot the bed
        ax1.plot(self.bed.distance_along_glacier, self.bed.bed_h,
                 label='Bedrock', ls=':', c='k', lw=2, zorder=3)
        # And fill it.
        ax1.fill_betweenx(self.bed.bed_h, self.bed.distance_along_glacier,
                          color='lightgrey')
        ax1.set_ylabel('Altitude [m]')

        # Set face color of side view.
        ax1.set_facecolor('#ADD8E6')
        ax1.set_ylim((self.bed.bottom, self.bed.top + 200))

        # Top down stuff
        # Fill the bed on the top down view.
        ax2.fill_between(self.bed.distance_along_glacier,
                         -self.bed.widths/2 * self.bed.map_dx,
                         self.bed.widths/2 * self.bed.map_dx,
                         color='lightgrey')
        ax2.axhline(0, c='k', zorder=3)
        ax2.set_facecolor('darkgrey')
        ax2.set_ylabel('Distance from centerline [m]')

        # If we have a current state, plot it.
        if self.current_state is not None:
            # Some masking shenanigans
            diff = self.current_state.surface_h - self.bed.bed_h
            mask = diff > 0
            idx = diff.argmin()
            mask[:idx+1] = True
            # Fill the glacier.
            ax1.fill_between(self.bed.distance_along_glacier,
                             self.bed.bed_h,
                             self.current_state.surface_h,
                             where=mask,
                             color='white',
                             lw=2)
            # Add outline
            ax1.plot(self.bed.distance_along_glacier[mask],
                     self.current_state.surface_h[mask],
                     lw=2,
                     label='Current glacier outline')
            # Fill in the glacier in the topdown view.
            # Where does the glacier have thickness?
            filled = np.where(self.current_state.thick > 0, self.bed.widths, 0)
            # Fill vetween them
            ax2.fill_between(self.bed.distance_along_glacier,
                             -filled/2 * self.bed.map_dx,
                             filled/2 * self.bed.map_dx,
                             where=filled > 0,
                             color='white',
                             edgecolor='C0',
                             lw=2
                             )
            ax1.set_ylim((self.bed.bottom,
                          self.current_state.surface_h[0] + 200))

        # ELA
        if self.ELA is not None:
            ax1.axhline(self.ELA, ls='--', c='k', lw=1)
            ax1.text(self.bed.distance_along_glacier[-1], self.ELA + 10,
                     'ELA', horizontalalignment='right',
                     verticalalignment='bottom')
            # Where along the bed is the ELA? Convert height to
            # distance along glacier kind of.
            idx = (np.abs(self.bed.bed_h - self.ELA)).argmin()
            # Plot the ELA in top down
            ax2.vlines(self.bed.distance_along_glacier[idx],
                       ymin=-self.bed.widths[idx]/2 * self.bed.map_dx,
                       ymax=self.bed.widths[idx]/2 * self.bed.map_dx,
                       color='k', ls='--', lw=1)

        # Limits etc
        plt.xlim((0, self.bed.distance_along_glacier[-1] + 2))

        # Decorations
        ax1.set_title(f'Glacier state at year {int(self.age)}')
        ax1.legend(loc='lower left')
        ax2.set_xlabel('Distance along glacier [km]')

    def plot_mass_balance(self):
        '''Plot the mass balance profile of the glacier'''
        plt.plot(self.annual_mass_balance(), self.bed.bed_h,
                 label='Mass balance',
                 c='tab:orange')
        plt.xlabel('Annual mass balance [m yr-1]')
        plt.ylabel('Altitude [m]')

        # Add ELA and 0 lines.
        plt.axvline(x=0, ls='--', lw=0.8, label='Mass balance = 0',
                    c='tab:green')
        plt.axhline(y=self.ELA, ls='--', lw=0.8, label='ELA',
                    c='tab:blue')
        plt.title('Mass balance profile')
        plt.legend()

    def plot_history(self):
        '''Plot the history of the glacier.'''
        if self.history is None:
            raise AttributeError('Glacier has no history yet,'
                                 ' try progress the glacier')

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

        # Plot the length.
        self.history.length_m.plot(ax=ax1)
        ax1.set_xlabel('')
        ax1.set_title(f'Glacier history at year {int(self.age)}')
        ax1.annotate('Glacier length', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax1.set_ylabel('Length [m]')
        # Plot the volume
        self.history.volume_m3.plot(ax=ax2)
        ax2.set_xlabel('')
        ax2.annotate('Glacier volume', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax2.set_ylabel('Volume [m$^3$]')
        # Plot the area
        self.history.area_m2.plot(ax=ax3)
        ax3.set_xlabel('Year')
        ax3.annotate('Glacier area', (0.98, 0.1), xycoords='axes fraction',
                     bbox={'boxstyle': 'Round', 'color': 'lightgrey'},
                     ha='right')
        ax3.set_ylabel('Area [m$^2$]')


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

        if glacier_list:
            if all(isinstance(glacier, Glacier) for glacier in glacier_list):
                self._glaciers = glacier_list

    def __repr__(self):
        return f'Glacier collection with {len(self.glaciers)} glaciers.'

    def check_collection(self, glacier):
        '''Utility method. Check if the glaciers obey the collection rules.
        They need to have the same domains for this to make sense I think.'''

    @property
    def glaciers(self):
        # Return the glaciers list.
        return self._glaciers

    # @glaciers.setter
    def add(self, glacier):
        '''Add a glacier to the collection.

        Parameters
        ----------
        glacier: oggm.edu Glacier object
        '''
        # Check that glacier is of the right type.
        if not isinstance(glacier, Glacier):
            raise TypeError('Glacier collection can only'
                            ' contain glacier objects.')
        # If the glacier is an instance of Glacier, we can add it to
        # the collection.
        else:
            self._glaciers.append(glacier)

    def progress_to_year(self, year):
        '''Grow the glaciers within the collection to year.

        Parameters
        ----------
        year: int
            Which year to grow the glaciers.
        '''
        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')

        for glacier in self.glaciers:
            glacier.progress_to_year(year)

    def progress_to_equilibrium(self):
        '''Grow the glaciers within the collection to equilibrium.
        '''
        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')

        for glacier in self.glaciers:
            glacier.progress_to_equilibrium()

    def plot(self):
        '''Plot the glaciers in the collection to compare them.'''

        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')
        # We use this to plot the bedrock etc.
        gl1 = self.glaciers[0]
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
        for i, glacier in enumerate(self.glaciers):
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

    def plot_history(self):
        '''Plot the histories of the collection'''

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

        for glacier in self.glaciers:
            # Plot the length.
            glacier.history.length_m.plot(ax=ax1)
            # Plot the volume
            glacier.history.volume_m3.plot(ax=ax2)
            # Plot the area
            glacier.history.area_m2.plot(ax=ax3,
                                         label=f'ELA: {glacier.ELA} \n' +
                                         f'MB grad: {glacier.mb_gradient} \n' +
                                         f'Age: {glacier.age}')
        # Decorations
        ax1.set_xlabel('')
        ax1.set_title('Glacier histories')
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
