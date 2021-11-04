'''This class provides a high level interface to the OGGM modelling framwork,
suitable for purely educational purposes, understanding the basics of
glacier mechanics.
'''

# Other libraries.
import numpy as np
import seaborn as sns
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
plt.rcParams['figure.figsize'] = (7, 5)


class Glacier:
    '''The glacier object'''

    def __init__(self, top, bottom, width, nx=200, map_dx=100):
        '''Initialise a glacier.

        Parameters
        ----------
        top : float
            Elevation at the top of the glacier domain in meters.
        bottom : float
            Elevation at the bottom of the glacier domain in meters.
        widths : float
            Width of the glacier in meters.
        nx : int
            Number of grid points.
        map_dx : int
            Grid point spacing in meters.
        '''

        # Geometry
        self.top = top
        self.bottom = bottom
        self.map_dx = map_dx
        self.width = width
        self.widths = (np.zeros(nx) + self.width) / map_dx
        # Initialise the bed
        self.bed_h = np.linspace(top, bottom, nx)
        self.surface_h = self.bed_h
        self.distance_along_glacier = np.linspace(0, nx, nx) * map_dx * 1e-3

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

    def __repr__(self):
        '''Pretty representation of the glacier object'''

        # Do we have a current state?
        state = self.state()
        string = f'Glacier at year {int(self.age)}' \
                 + f'\nTop eleveation {self.top} m.a.s.l.' \
                 + f'\nBottom elevation {self.bottom} m.a.s.l' \
                 + f'\nELA: {self.ELA}' \
                 + f'\nWidth {self.width} m.\nLength {state.length_m} m.' \
                 + f'\nArea {state.area_km2:.3f} km2.\nVolume' \
                 + f' {state.volume_km3:.3f} km3'
        return string

    def init_flowline(self):
        return RectangularBedFlowline(surface_h=self.surface_h,
                                      bed_h=self.bed_h,
                                      widths=self.widths, map_dx=self.map_dx)

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

    def grow_to_year(self, year):
        '''Method to grow the glacier for n years.

        Parameters
        ----------
        year : int
            Year until which to grow the glacier.
        '''
        # Check if the glacier has a masss balance model
        if not self.mb_model:
            string = 'To grow the glacier it needs a mass balance.' \
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
                model.run_until(year)
            except RuntimeError:
                print('Glacier outgrew its domain and had to stop.')
                # raise RuntimeError('Glacier grew outside its domain.'
                #                    + ' Try raising the ELA.')

            self.current_state = model.fls[0]
            self.model_state = model
            self.age = model.yr

    def grow_to_equilibrium(self):
        'Method to grow the glacier to equilibrium.'
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
                model.run_until_equilibrium()
            except RuntimeError:
                print('Glacier grew out of its domain and had to stop.')
                # raise RuntimeError('Glacier grew outside its domain.'
                #                    + ' Try raising the ELA.')

            self.current_state = model.fls[0]
            self.age = model.yr
            self.model_state = model

    def plot(self):
        '''Plot the glacier'''
        # Bedrock
        plt.plot(self.distance_along_glacier, self.bed_h, label='Bedrock',
                 ls=':', c='k', lw=2, zorder=3)
        plt.fill_betweenx(self.bed_h, self.distance_along_glacier,
                          facecolor='grey', alpha=0.3)
        # Plot the initial galcier surface
        plt.plot(self.distance_along_glacier, self.initial_state.surface_h,
                 label='Initial glacier surface height', c='tab:orange')
        # If we have a current state, plot it.
        if self.current_state is not None:
            plt.plot(self.distance_along_glacier, self.current_state.surface_h,
                     label='Current glacier surface height')

        # ELA
        if self.ELA is not None:
            plt.axhline(self.ELA, ls='--', c='k', lw=1)
            plt.text(self.distance_along_glacier[-1], self.ELA + 10,
                     'ELA', horizontalalignment='right',
                     verticalalignment='bottom')

        # Decorations
        plt.xlabel('Distance along glacier [km]')
        plt.ylabel('Altitude [m]')
        plt.title(f'Glacier state at year {int(self.age)}')
        plt.legend(loc='lower left')

    def plot_mass_balance(self):
        '''Plot the mass balance profile of the glacier'''
        plt.plot(self.annual_mass_balance(), self.bed_h, label='Mass balance',
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

    def grow_to_year(self, year):
        '''Grow the glaciers within the collection to year.

        Parameters
        ----------
        year: int
            Which year to grow the glaciers.
        '''
        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')

        for glacier in self.glaciers:
            glacier.grow_to_year(year)

    def grow_to_equilibrium(self):
        '''Grow the glaciers within the collection to equilibrium.
        '''
        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')

        for glacier in self.glaciers:
            glacier.grow_to_equilibrium()

    def plot(self):
        '''Plot the glaciers in the collection to compare them.'''

        if len(self.glaciers) < 1:
            raise ValueError('Collection is empty')
        # We use this to plot the bedrock etc.
        gl1 = self.glaciers[0]
        # Get the ax from the first plot
        fig, ax = plt.subplots()
        # Bedrock
        ax.plot(gl1.distance_along_glacier, gl1.bed_h, label='Bedrock',
                ls=':', c='k', lw=2, zorder=3)
        # Fill it in.
        ax.fill_betweenx(gl1.bed_h, gl1.distance_along_glacier,
                         facecolor='grey', alpha=0.3)

        # Set the title.
        ax.set_title('Glacier collection')

        elas = []
        # Loop over the collection.
        for i, glacier in enumerate(self.glaciers):
            # Plot the surface
            if glacier.current_state is not None:
                ax.plot(glacier.distance_along_glacier,
                        glacier.current_state.surface_h,
                        label=f'Glacier nr. {i+1} at year {glacier.age}')
            elas.append(glacier.ELA)

        # Loop the unique ELAs.
        for i, ela in enumerate(set(elas)):
            # Plot the ELA
            ax.axhline(ela, ls='--', zorder=1, alpha=0.3)
            # Label if elas are equal.
            if len(set(elas)) == 1:
                ax.text(glacier.distance_along_glacier[-1], ela + 10,
                        'ELAs are equal', ha='right', va='bottom')
            # If we have multiple ELAs.
            else:
                ax.text(glacier.distance_along_glacier[-1], ela + 10,
                        f'ELA  nr {i+1}', ha='right', va='bottom')

        # axis labels.
        ax.set_xlabel('Distance along glacer [km]')
        ax.set_ylabel('Altitude [m]')
        plt.legend(loc='lower right')
