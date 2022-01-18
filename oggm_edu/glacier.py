'''This module provides a high level interface to the OGGM modelling framwork,
suitable for educational purposes regarding the understanding the basics of
glacier mechanics.

It contains two classes: Glacier and SurgingGlacier, the top-level interfaces
to experimenting with glaciers through OGGM-Edu. Initialisation depends on
two other classes: the GlacierBed and the MassBalance.
'''

# Internals
from oggm_edu.glacierBed import GlacierBed
from oggm_edu.massBalance import MassBalance

# Other libraries.
import numpy as np
import seaborn as sns
import xarray as xr
import pandas as pd
import warnings
import copy
from itertools import cycle

# Plotting
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
# Import OGGM things.
from oggm.core.flowline import FluxBasedModel, RectangularBedFlowline

from oggm import cfg
# Initialise cfg
cfg.initialize_minimal()
sns.set_context('notebook')
sns.set_style('ticks')
plt.rcParams['figure.figsize'] = (12, 9)


class Glacier:
    '''The glacier object'''

    def __init__(self, bed=None, mass_balance=None):
        '''Initialise a glacier object. Either from a glacier bed
        or from an already existing glaicer.

        Parameters
        ----------
        bed : GlacierBed object

        mass_balance : MassBalance object
            Optional
        '''
        # If we pass a bed, initialise a new glacier.
        if bed:
            # Check the type of the bed.
            if not isinstance(bed, GlacierBed):
                raise TypeError('The bed has to be of the type GlacierBed.')
            # Set the bed.
            self.bed = bed
            # Set the surface height.
            self.surface_h = self.bed.bed_h

            # Mass balance
            self._mass_balance = None
            # The following two attributes are just used when we set the mass
            # balance in steps.
            self._ELA_assign = None
            self._mb_grad_assign = None

            # If mass balance object is provided, and of type MassBalance
            if mass_balance and isinstance(mass_balance, MassBalance):
                self._mass_balance = mass_balance

            elif mass_balance and not isinstance(mass_balance, MassBalance):
                raise TypeError('Mass balance supplied but not of the' +
                                ' correct type.')

            # Initilaise the flowline
            self.initial_state = self.init_flowline()
            # Set current and model state to None.
            self.current_state = None
            self.model_state = None

            # Ice dynamics parameters
            # Sane defaults
            self._basal_sliding = 0.
            self._creep = cfg.PARAMS['glen_a']

            # Descriptives
            # Store the age of the glacier outside the model object.
            self._age = 0
            # This is used to store the history of the glacier evolution.
            #  None for now.
            self._history = None
            # Store the state history
            self._state_history = None

            # We want to save the eq. states.
            self._eq_states = []

        # if nothing works
        else:
            raise ValueError('Provide a bed.')

    def __repr__(self):
        '''Pretty representation of the glacier object'''

        # Get the json representation.
        json = self._to_json()
        # Create the string
        string = 'Glacier \n'
        for key, value in json.items():
            string += f'{key}: {value} \n'
        string += repr(self.bed)
        string += repr(self.mass_balance)
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
        '''Json represenation'''
        state = self.state()
        json = {'Age': int(self.age),
                'Length [m]': state.length_m,
                'Area [km2]': state.area_km2,
                'Volume [km3]': state.volume_km3,
                }
        return json

    def copy(self):
        '''Return a deepcopy of the glacier. Useful for creating
        new glaciers.'''
        return copy.deepcopy(self)

    def init_flowline(self):
        # Initialise a RectangularBedFlowline for the glacier.
        return RectangularBedFlowline(surface_h=self.surface_h,
                                      bed_h=self.bed.bed_h,
                                      widths=self.bed.widths,
                                      map_dx=self.bed.map_dx)

    @property
    def ELA(self):
        try:
            return self.mass_balance.ela_h
        except AttributeError:
            return None

    @ELA.setter
    def ELA(self, value):
        '''Define the equilibrium line altitude.

        Parameters
        ----------
        value : int or float
            Altitude of the ELA.
        '''
        # We cant have a negative ELA.
        if value < 0:
            raise ValueError('ELA below 0 not allowed.')

        self._ELA_assign = value
        # If we have the gradient, set the mb_model
        if self._mb_grad_assign:
            self._mass_balance = MassBalance(self._ELA_assign,
                                             self._mb_grad_assign)

    @property
    def mb_gradient(self):
        try:
            return self.mass_balance.grad
        except AttributeError:
            return None

    @mb_gradient.setter
    def mb_gradient(self, value):
        '''Define the mass balance gradient.

        Parameters
        ----------
        value : int or float
            Mass balance altitude gradient, mm/m.
        '''
        # We cant have a negative gradient.
        if value < 0:
            raise ValueError('Mass balance gradient less than 0 not allowed')

        self._mb_grad_assign = value
        # If we have the ELA, set the mb_model
        if self._ELA_assign:
            self._mass_balance = MassBalance(self._ELA_assign,
                                             self._mb_grad_assign)

    @property
    def mass_balance(self):
        return self._mass_balance

    def annual_mass_balance(self):
        return self.mass_balance.get_annual_mb(self.surface_h)\
            * cfg.SEC_IN_YEAR

    def state(self):
        '''Glacier state logic'''
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
        '''Set the age of the glacier.'''
        self._age = int(value)

    @property
    def history(self):
        '''Return the glacier history dataset.'''
        return self._history

    @property
    def state_history(self):
        return self._state_history

    @state_history.setter
    def state_history(self, obj):
        '''Setting/updating the state history'''
        # Is there any state history yet?
        if self.state_history is None:
            self._state_history = obj
        # If there is, append instead.
        else:
            # We slice the new series because we dont need the first year.
            self._state_history = xr.combine_by_coords([
                self.state_history.isel(time=slice(0, -1)), obj
            ], combine_attrs='override')

    @property
    def basal_sliding(self):
        return self._basal_sliding

    @basal_sliding.setter
    def basal_sliding(self, value):
        '''Set the sliding parameter of the glacier

        Parameters
        ----------
        value : float
            Value fo the glacier sliding
        '''
        self._basal_sliding = value

    @property
    def creep(self):
        return self._creep

    @creep.setter
    def creep(self, value):
        '''Set the value for glen_a creep

        Parameters
        ----------
        value : float
        '''
        self._creep = value

    @history.setter
    def history(self, obj):
        '''Logic for the glacier history attribute. If there is no histoy,
        we add it. If the glacier already has some history, we append it.'''
        # Does it have any history?
        if self._history is None:
            self._history = obj
        # Append the history.
        else:
            # We slice the new series because we dont need the first year.
            self._history = xr.combine_by_coords([
                self.history.isel(time=slice(0, -1)), obj
            ], combine_attrs='override')

    @property
    def eq_states(self):
        if len(self._eq_states) == 0:
            print("The glacier have not reached equilibrium yet.")
        else:
            return self._eq_states

    @property
    def response_time(self):
        '''Returns the reponse time of the glacier.
        Calculates the volume response time from Oerlemans based on the
        two latest eq. states.'''

        # If we don't hace a eq. states yet
        if len(self._eq_states) < 2:
            raise AttributeError("Glacier don't have a response time yet." +
                  " The glacier needs two equilibrium states.")
        else:
            # We calcuate the response time when we need it.
            # Not sure if this is stupid but.
            # Final eq. volume
            v_final = self.history.volume_m3.sel(time=self.eq_states[-1])
            # Initial volume
            v_initial = self.history.volume_m3.sel(time=self.eq_states[-2])
            # Volume difference
            v_diff = v_final - (v_final - v_initial) / np.e
            # Find the year where volume is closest to the v_diff.
            all_vol_diff = np.abs(self.history.volume_m3.sel(
                time=slice(self.eq_states[-2], self.eq_states[-1])
            ) - v_diff)
            # Get the index
            idx = all_vol_diff.argmin()
            # Reponse time
            response_time = all_vol_diff.time.isel(time=idx) -\
                self.eq_states[-2]
            return response_time.values.item()

    def add_temperature_bias(self, bias, duration):
        '''Add a temperature bias to the mass balance of the glacier.

        Parameters
        ----------
        bias: float
            Temperature bias to apply
        duration: int
            Specify during how many years the bias will be applied.
        '''
        self.mass_balance._add_temp_bias(bias, duration, self.age)

    def progress_to_year(self, year):
        '''Method to progress the glacier to year n.
        Parameters
        ----------
        year : int
            Year until which to progress the glacier.
        '''
        # Check if the glacier has a masss balance model
        if not self.mass_balance:
            string = 'To evolve the glacier it needs a mass balance.' \
                      + '\nMake sure the ELA and mass balance gradient' \
                      + ' are defined.'
            raise NotImplementedError(string)

        # Some checks on the year.
        elif year < 0:
            raise ValueError('Year has to be above zero')

        elif year <= self.age:
            warnings.warn('Year has to be above the current age of'
                          + ' the glacier. It is not possible to'
                          + ' de-age the glacier.'
                          + ' Geometry will remain.')

        # If all passes
        else:
            # Do we have any years left to run?
            while year - self.age > 0:
                # Check if we have a current state already.
                state = self.state()
                # Initialise the model
                model = FluxBasedModel(state, mb_model=self.mass_balance,
                                       y0=self.age, glen_a=self.creep,
                                       fs=self.basal_sliding)
                # If we have temp evolution left to do.
                if self.age < self.mass_balance._temp_bias_final_year:
                    # Run the model. Store the history.
                    # How big are the steps?
                    run_to = int(self.age + 1)
                    try:
                        out = model.run_until_and_store(run_to,
                                                        fl_diag_path=None)
                    except RuntimeError:
                        raise RuntimeError('Glacier outgrew its domain and' +
                                           ' had to stop')
                    self.mass_balance._update_temp_bias(model.yr)
                # If there is no temp evolution, do all the years.
                else:
                    # Run the model. Store the history.
                    try:
                        out = model.run_until_and_store(year,
                                                        fl_diag_path=None)
                    except RuntimeError:
                        raise RuntimeError('Glacier outgrew its domain and' +
                                           ' had to stop')

                # Update attributes.
                self.history = out[0]
                self.state_history = out[1][0]
                self.current_state = model.fls[0]
                self.model_state = model
                self.age = model.yr

    def progress_to_equilibrium(self, years=2500):
        '''Progress the glacier to equilibrium.

        Parameters
        ----------
        years : int, optional
            Specify the number of years during which we try to find
            an equilibrium state.
        '''

        def stop_function(model, previous_state):
            '''Function to stop the simulation when equilbrium is
            reached. Basically a re-shape of the criterium of
            run_until_equilibrium.'''
            # We don't stop unless
            stop = False
            # Ambigous rate, basically how fast is the glacier
            # changing every step.
            rate = 0.001
            # How many times to we try
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
                # Dictionary containing the stuff we need.
                previous_state = {'ite': 0, 'was_close_zero': 0,
                                  't_rate': 1,
                                  'v_bef': model.volume_m3}

            return stop, previous_state

        # Check if the glacier has a masss balance model
        if not self.mass_balance:
            string = 'To grow the glacier it needs a mass balance.' \
                      + '\nMake sure the ELA and mass balance gradient' \
                      + ' are defined.'
            raise NotImplementedError(string)

        else:
            # Do we have a temp scenario which isn't passed yet?
            if self.age < self.mass_balance._temp_bias_final_year:
                # If so, progress normally.
                self.progress_to_year(self.mass_balance._temp_bias_final_year)
            # Then we can find the eq. state.
            # Initialise the model
            state = self.state()
            model = FluxBasedModel(state, mb_model=self.mass_balance,
                                   y0=self.age, glen_a=self.creep,
                                   fs=self.basal_sliding)
            # Run the model.
            try:
                #  Run with a stopping criteria.
                out = model.run_until_and_store(years,
                                                fl_diag_path=None,
                                                stop_criterion=stop_function)

            except RuntimeError:
                print('Glacier grew out of its domain and had to stop.')

            # Update attributes.
            self.history = out[0].dropna(dim='time')
            self.state_history = out[1][0].dropna(dim='time')
            self.current_state = model.fls[0]
            self.age = model.yr
            self.model_state = model
            # Remember the eq. year
            self._eq_states.append(self.age)

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
            if self.current_state is not None:
                idx = (np.abs(self.current_state.surface_h -
                              self.ELA)).argmin()
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

    def _create_history_plot_components(self):
        '''Create components for the history plot of the glacier.'''
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

        # Grid
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)

        return fig, ax1, ax2, ax3

    def plot_history(self):
        '''Plot the history of the glacier'''
        # Get the components
        fig, ax1, ax2, ax3 = self._create_history_plot_components()
        plt.show()

    def plot_state_history(self, interval=50):
        '''Plot the state history of the glacier (thicknesses) at specified
        intervals.

        Parameters
        ----------
        interval: int
            Specifies the number of years between each states in the plot.
        '''
        # Get the base plotting components from the bed.
        fig, ax1, ax2 = self.bed._create_base_plot()

        # We need a manual color cycle for the top down view.
        prop_cycle = plt.rcParams['axes.prop_cycle']
        colors = cycle(prop_cycle.by_key()['color'])

        # Want to plot thickness at specified intervals. So we slice it.
        states = self.state_history.thickness_m.\
            isel(time=slice(interval, -1, interval))
        # Loop over states.
        for i, state in enumerate(states):
            # Some masking shenanigans
            mask = state.values > 0
            idx = state.values.argmin()
            mask[:idx+1] = True
            # Fill the glacier.
            ax1.fill_between(self.bed.distance_along_glacier,
                             self.bed.bed_h,
                             state.values + self.bed.bed_h,
                             where=mask,
                             color='white',
                             lw=2)
            # Add outline
            # Modify the zorder to get lines to show up nice.
            ax1.plot(self.bed.distance_along_glacier[mask],
                     state[mask] + self.bed.bed_h[mask],
                     lw=2,
                     label=f'Glacier outline at year {interval+i*interval}',
                     zorder=4-i*0.1)
            # Fill in the glacier in the topdown view.
            # Where does the glacier have thickness?
            filled = np.where(state > 0, self.bed.widths, 0)
            # Fill vetween them
            # Modify the zorder to get lines to show up nice.
            ax2.fill_between(self.bed.distance_along_glacier,
                             -filled/2 * self.bed.map_dx,
                             filled/2 * self.bed.map_dx,
                             where=filled > 0,
                             facecolor='white',
                             edgecolor=next(colors),
                             lw=2,
                             zorder=2-i*0.1
                             )
        # New title.
        ax1.set_title('Glacier states')
        # Update the legend.
        ax1.legend()
        plt.show()


class SurgingGlacier(Glacier):
    '''A surging glacier. This will have the same attributes as a normal
    glacier but with some extensions e.g. normal years and surging years.
    '''

    def __init__(self, bed):
        '''Initialise the surging glacier. Inherit attributes and methods
        from the Glacier class and extend it with some attributes specific
        for surging glaciers.
        '''

        # Inherit from glacier
        super().__init__(bed)

        # Surging attributes
        self._normal_years = 50
        self._surging_years = 5
        # Basal sliding during surge has a sane default.
        # So no need to touch it.
        self._basal_sliding_surge = 5.7e-20 * 10
        # Some state attributes used by the progress method
        # to determine if we are surging or normal
        self._normal_period = True
        self._normal_years_left = self.normal_years
        self._surging_years_left = self.surging_years

    def _to_json(self):
        '''Json represenation'''
        state = self.state()
        json = {'Age': int(self.age),
                'Length [m]': state.length_m,
                'Area [km2]': state.area_km2,
                'Volume [km3]': state.volume_km3,
                'Surging periodicity (off/on)':
                (self.normal_years, self.surging_years),
                'Surging now?': not self._normal_period
                }
        return json

    @property
    def normal_years(self):
        '''Number of years that the glacier progress without surging.'''
        return self._normal_years

    @normal_years.setter
    def normal_years(self, value):
        '''Set the length of the normal period.

        Parameters
        ----------
        value : int
            Length of the normal period.
        '''
        if value > 0 and isinstance(value, int):
            self._normal_years = value
            self._normal_years_left = value
        else:
            raise ValueError('Normal years should be above 0 and' +
                             ' and of the type integer.')

    @property
    def surging_years(self):
        '''Number of years that the glacier progress during surges.'''
        return self._surging_years

    @surging_years.setter
    def surging_years(self, value):
        '''Set the length of the surging period.

        Parameters
        ----------
        value : int
            Length of surging period.
        '''
        if value > 0 and isinstance(value, int):
            self._surging_years = value
            self._surging_years_left = value
        else:
            raise ValueError('Surging years should be above 0 and' +
                             ' and of the type integer.')

    @property
    def basal_sliding_surge(self):
        return self._basal_sliding_surge

    @basal_sliding_surge.setter
    def basal_sliding_surge(self, value):
        self._basal_sliding_surge = value

    def progress_to_year(self, year):
        '''Progress the surging glacier to specified year.
        This will progress the glacier in periods of surging
        and not surging, specified by the `normal_years` and
        `surging_years` attributes.

        Parameters:
        -----------
        year : int
            Which year to progress the surging glacier.
        '''

        # Check if the glacier has a masss balance model
        if not self.mass_balance:
            string = 'To evolve the glacier it needs a mass balance.' \
                      + '\nMake sure the ELA and mass balance gradient' \
                      + ' are defined.'
            raise NotImplementedError(string)

        # Some checks on the year.
        elif year < 0:
            raise ValueError('Year has to be above zero')

        elif year <= self.age:
            warnings.warn('Year has to be above the current age of'
                          + ' the glacier. It is not possible to'
                          + ' de-age the glacier.'
                          + ' Geometry will remain.')

        # If all passes
        else:
            # How many years to have left to simulate
            years_left = year - self.age
            # While we have years to run we do the following...
            while years_left:
                # Check if we have a current state already.
                state = self.state()
                # If in a normal period
                if self._normal_period:
                    # How many years should we run?
                    # We either run for the normal period amount of
                    # yeasrs. Or for the years left we have left.
                    # or the normal years left from a previous run.
                    years_to_run = np.min([years_left,
                                           self.normal_years,
                                           self._normal_years_left])
                    # Cast to int
                    years_to_run = int(years_to_run + self.age)
                    # Update normal_years_left
                    self._normal_years_left -= (years_to_run - self.age)
                    # If we have no normal years left we change state.
                    if self._normal_years_left == 0:
                        # Re-set it
                        self._normal_years_left = self.normal_years
                        # Not normal anymore
                        self._normal_period = not self._normal_period

                    # Initialise the model, width the normal basal_slidng
                    model = FluxBasedModel(state, mb_model=self.mass_balance,
                                           y0=self.age, glen_a=self.creep,
                                           fs=self.basal_sliding)
                    # Run the model. Store the history.
                    try:
                        out = model.run_until_and_store(years_to_run,
                                                        fl_diag_path=None)
                    except RuntimeError:
                        print('Glacier outgrew its domain and had to stop.')
                        # We should break here.
                        break

                # If we are not in normal state, we do a surging period.
                else:
                    # How many years should we run?
                    # Same as above but now we run for surging period amount
                    # of years.
                    years_to_run = np.min([years_left,
                                           self.surging_years,
                                           self._surging_years_left])
                    # Cast to int
                    years_to_run = int(years_to_run + self.age)
                    #  Update surging years left
                    self._surging_years_left -= (years_to_run - self.age)
                    # If there are no surging years left, we change state
                    if self._surging_years_left == 0:
                        # Re-set
                        self._surging_years_left = self.surging_years
                        # Not surging anymore
                        self._normal_period = not self._normal_period

                    # Initialise the model, with the surging basal_sliding
                    model = FluxBasedModel(state, mb_model=self.mass_balance,
                                           y0=self.age, glen_a=self.creep,
                                           fs=self.basal_sliding_surge)
                    # Run the model. Store the history.
                    try:
                        out = model.run_until_and_store(years_to_run,
                                                        fl_diag_path=None)
                    except RuntimeError:
                        print('Glacier outgrew its domain and had to stop.')
                        # We should break here.
                        break

                # Update attributes.
                self.history = out[0]
                self.state_history = out[1][0]
                self.current_state = model.fls[0]
                self.model_state = model
                self.age = model.yr
                # Check where we are
                years_left = year - self.age

    def progress_to_equilibrium(self):
        '''Surging glaciers do not really have an eq. state.'''
        raise NotImplementedError('Surging glaciers do not progress to' +
                                  ' equilibrium. Yet...')

    def plot_history(self):
        '''Plot the history of the surging glacier.
        Extends the Glacier.plot_history() method.'''
        # Get the base plotting components.
        fig, ax1, ax2, ax3 = self._create_history_plot_components()

        # We then want to add markers for the surging years.
        # How many surges do we have?
        nr_surges = int(self.age / (self.normal_years +
                                    self.surging_years))
        # Loop over the surges
        for i in range(nr_surges):
            # When should the span start
            start = (i+1) * self.normal_years +\
                i * self.surging_years
            # and end.
            end = (i + 1) * self.normal_years +\
                self.surging_years + i * self.surging_years
            # Add spans
            ax1.axvspan(start, end, color='tab:orange', alpha=0.3)
            ax2.axvspan(start, end, color='tab:orange', alpha=0.3)
            ax3.axvspan(start, end, color='tab:orange', alpha=0.3)

        # Legend entry
        patch = Patch(facecolor='tab:orange', alpha=0.3,
                      label='Surging period')
        fig.legend(handles=[patch], loc='upper left',
                   bbox_to_anchor=(0.9, 0.89))

        plt.show()
