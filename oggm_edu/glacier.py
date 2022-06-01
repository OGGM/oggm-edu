"""This module provides a high level interface to the OGGM modelling framework,
suitable for educational purposes regarding the understanding the basics of
glacier mechanics.

It contains two classes: Glacier and SurgingGlacier, the top-level interfaces
to experimenting with glaciers through OGGM-Edu. Initialisation depends on
two other classes: the GlacierBed and the MassBalance.
"""

# Internals
from oggm_edu.glacier_bed import GlacierBed
from oggm_edu.mass_balance import MassBalance
from oggm_edu.funcs import edu_plotter

# Other libraries
import numpy as np
import xarray as xr
import pandas as pd
import warnings
import copy
from itertools import cycle
import re
from collections.abc import Sequence

# Plotting
from matplotlib import pyplot as plt
from matplotlib.patches import Patch

# Import OGGM things
from oggm.core.flowline import FluxBasedModel, RectangularBedFlowline
from oggm import cfg


class Glacier:
    """Provides the user with an easy way to create and perform experiments on
    simulated glaciers.

    It handles the progression and visualisation of the glacier. A glacier is constructed
    with a GlacierBed and MassBalance.


    Attributes
    ----------
    age : int
        The age of the glacier.
    annual_mass_balance : array
        The annual mass balance at each grid point of the glacier.
    basal_sliding : float
        Basal sliding of the glacier.
    bed : oggm_edu.GlacierBed
        The bed of the glacier.
    creep : float
        Ice creep parameter (a in Glenns flow law).
    eq_states : dict
        Dictionary where key-value pairs represent the year and ELA height of the equilibrium states of
        the glacier.
    history : xArray dataset
        Dataset containing the 1D history (time) of the glacier, notably length, area and volume.
    mass_balance : oggm_edu.MassBalance
        The mass balance of the glacier.
    specific_mass_balance : float
        Specific mass balance of the glacier [m w.e. yr^-1].
    state_history : xArray dataset
        Dataset containing the 2D state history (time, length) of the glacier, notably the surface height.
    response_time : int
        The time it takes for the glacier reach a new equilibrium state after a change in climate.
        Calculates the volume response time from Oerlemans.
    """

    def __init__(self, bed, mass_balance):
        """Initialise a glacier object from a oggm_edu.GlacierBed and a oggm_edu.MassBalance.

        Parameters
        ----------
        bed : oggm_edu.GlacierBed
        mass_balance : oggm_edu.MassBalance
        """
        # Check input
        if not isinstance(bed, GlacierBed):
            raise TypeError("The bed has to be of type GlacierBed.")

        # Set the bed.
        self.bed = copy.deepcopy(bed)
        # Set the surface height.
        self.surface_h = self.bed.bed_h

        # Mass balance
        # If mass balance is of the wrong type.
        if not isinstance(mass_balance, MassBalance):
            raise TypeError("mass_balance should be of the type oggm_edu.MassBalance.")

        self._mass_balance = copy.deepcopy(mass_balance)

        # Initilaise the flowline
        self._initial_state = self._init_flowline()
        # Set current and model state to None.
        self._current_state = None
        self._model_state = None

        # Ice dynamics parameters
        # Sane defaults
        self._basal_sliding = 0.0
        self._creep = cfg.PARAMS["glen_a"]

        # Descriptives
        # Store the age of the glacier outside the model object.
        self._age = 0
        # This is used to store the history of the glacier evolution.
        #  None for now.
        self._history = None
        # Store the state history
        self._state_history = None

        # We want to save the eq. states.
        self._eq_states = {}

    def __repr__(self):
        """Pretty representation of the glacier object"""

        # Get the json representation.
        json = self._to_json()
        # Create the string
        string = "Glacier \n"
        for key, value in json.items():
            string += f"{key}: {value} \n"
        string += repr(self.bed)
        string += repr(self.mass_balance)
        return string

    def _repr_html_(self):
        """HTML representations"""
        # Return the html representation of the summary df,
        return self.summary()._repr_html_()

    def summary(self):
        """A summary of the glacier, in the form of a pandas dataframe."""
        # Get attris
        attrs = self._to_json()
        # Create the dataframe.
        df = pd.DataFrame.from_dict(attrs, orient="index")
        df.columns = [""]
        df.index.name = "Attribute"
        # Return the df.
        return df

    def reset(self):
        """Reset the glacier to initial state."""
        # Just force attributes to initials.
        self._current_state = None
        self._model_state = None
        # Surface height.
        self.surface_h = self.bed.bed_h
        # Forget history.
        self._history = None
        self._state_history = None
        self._eq_states = {}
        # Age
        self._age = 0
        # Ice params.
        self._basal_sliding = 0.0
        self._creep = cfg.PARAMS["glen_a"]
        # Reset the mass balance.
        self._mass_balance.reset()

    def _to_json(self):
        """Json represenation"""
        state = self._state()

        # Do we have a state history yet?
        if self.state_history:
            ice_vel = self.state_history.ice_velocity_myr.max().values
        else:
            ice_vel = None
        json = {
            "Type": type(self).__name__,
            "Age": int(self.age),
            "Length [m]": state.length_m,
            "Area [km2]": state.area_km2,
            "Volume [km3]": state.volume_km3,
            "Max ice thickness [m]": state.thick.max(),
            "Max ice velocity [m/yr]": ice_vel,
            "Response time [yrs]": self.response_time,
        }
        return json

    def copy(self):
        """Return a copy of the glacier. Useful for quickly creating
        new glaciers."""
        return copy.deepcopy(self)

    def _init_flowline(self):
        # Initialise a RectangularBedFlowline for the glacier.
        return RectangularBedFlowline(
            surface_h=self.surface_h,
            bed_h=self.bed.bed_h,
            widths=self.bed.widths,
            map_dx=self.bed.map_dx,
        )

    @property
    def ela(self):
        "Expose the mass balance ela for the glacier."
        return self.mass_balance.ela_h

    @property
    def mb_gradient(self):
        "Expose the mass balance gradient."
        return self.mass_balance.gradient

    @property
    def mass_balance(self):
        "Glacier mass balance."
        return self._mass_balance

    @property
    def annual_mass_balance(self):
        """The annual mass balance at each grid point of the glacier."""
        return self.mass_balance.get_annual_mb(self.surface_h) * cfg.SEC_IN_YEAR

    @property
    def specific_mass_balance(self):
        """The specific mass balance of the glacier [m w.e. yr^-1]."""
        # Only want data where there is ice.
        mask = self._state().thick > 0

        # Get the mb where there is ice.
        mb_s = self.annual_mass_balance[mask] * cfg.PARAMS["ice_density"]
        # Take the weighted average, since glacier has different widths.
        mb_s = np.average(mb_s, weights=self.bed.widths[mask])

        # Return the m. w.e.
        return mb_s / 1000.0

    def _state(self):
        """Glacier state logic"""
        state = self._initial_state
        # If we have a current state
        if self.current_state:
            state = self.current_state
        return state

    @property
    def current_state(self):
        """For advanced users: get access to the current OGGM ``Flowline`` object."""
        return self._current_state

    @property
    def age(self):
        """Set the age of the glacier."""
        return self._age

    @age.setter
    def age(self, value):
        """Set the age of the glacier."""
        self._age = int(value)

    @property
    def history(self):
        """The history of the glacier. Contains the history of notably
        the length, area and volume of the glacier.
        """
        return self._history

    @property
    def state_history(self):
        """The state history of the glacier, i.e. geometrical changes over time.
        For instance ice thickness.
        """
        return self._state_history

    @state_history.setter
    def state_history(self, obj):
        """Setting/updating the state history"""
        # Is there any state history yet?
        if self.state_history is None:
            self._state_history = obj
        # If there is, append instead.
        else:
            # We slice the new series because we dont need the first year.
            self._state_history = xr.combine_by_coords(
                [self.state_history.isel(time=slice(0, -1)), obj],
                combine_attrs="override",
            )

    @property
    def basal_sliding(self):
        """Set the sliding parameter of the glacier"""
        return self._basal_sliding

    @basal_sliding.setter
    def basal_sliding(self, value):
        """Set the sliding parameter of the glacier

        Parameters
        ----------
        value : float
            Value fo the glacier sliding
        """
        self._basal_sliding = value

    @property
    def creep(self):
        """Set the value for glen_a creep"""
        return self._creep

    @creep.setter
    def creep(self, value):
        """Set the value for glen_a creep

        Parameters
        ----------
        value : float
        """
        self._creep = value

    @history.setter
    def history(self, obj):
        """Logic for the glacier history attribute. If there is no histoy,
        we add it. If the glacier already has some history, we append it."""
        # Does it have any history?
        if self._history is None:
            self._history = obj
        # Append the history.
        else:
            # We slice the new series because we dont need the first year.
            self._history = xr.combine_by_coords(
                [self.history.isel(time=slice(0, -1)), obj],
                combine_attrs="override",
            )

    @property
    def eq_states(self):
        """Glacier equilibrium states."""
        if not self._eq_states:
            print("The glacier have not reached equilibrium yet.")
        else:
            return self._eq_states

    @property
    def response_time(self):
        """The response time of the glacier.

        Calculates the volume response time from Oerlemans based on the
        two latest eq. states.
        """

        # If we don't hace a eq. states yet
        if len(self._eq_states) < 2:
            return np.nan
        else:
            # We calcuate the response time when we need it.
            # Not sure if this is stupid but.
            # Get the eq state years.
            year_final = list(self.eq_states)[-1]
            year_initial = list(self.eq_states)[-2]
            # Final eq. volume
            v_final = self.history.volume_m3.sel(time=year_final)
            # Initial volume
            v_initial = self.history.volume_m3.sel(time=year_initial)
            # Volume difference
            v_diff = v_final - (v_final - v_initial) / np.e
            # Find the year where volume is closest to the v_diff.
            all_vol_diff = np.abs(
                self.history.volume_m3.sel(time=slice(year_initial, year_final))
                - v_diff
            )
            # Get the index
            idx = all_vol_diff.argmin()
            # Reponse time
            response_time = all_vol_diff.time.isel(time=idx) - year_initial
            return response_time.values.item()

    def add_temperature_bias(self, bias, duration, noise=None):
        """Add a gradual temperature bias to the future mass balance of the
        glacier. Note that the method is cumulative, i.e. calling it multiple
        times will extend the prescribed climate.
        glacier.

        Parameters
        ----------
        bias : float
            Temperature bias to apply
        duration: int
            Specify during how many years the bias will be applied.
        noise : list(float, float)
            Sequence of floats which defines the lower and upper boundary of
            the random noise to add to the trend.
        """
        self.mass_balance.add_temp_bias(bias, duration, noise)

    def add_random_climate(self, duration, temperature_range):
        """Append a random climate to the future mass balance of the glacier.
        Note that the method is cumulative, i.e. calling it multiple
        times will extend the prescribed climate.

        Parameters
        ----------
        duration : int
            How many years should the random climate be.
        temperature_range : array_like(float, float)
            The range over which the climate should vary randomly.
        """
        self.mass_balance.add_random_climate(duration, temperature_range, self.age)

    def progress_to_year(self, year):
        """Progress the glacier to year n.

        Parameters
        ----------
        year: int
            Year until which to progress the glacier.
        """
        # Some checks on the year.
        if year < 0:
            raise ValueError("Year has to be above zero")

        elif year <= self.age:
            warnings.warn(
                "Year has to be above the current age of"
                + " the glacier. It is not possible to"
                + " de-age the glacier."
                + " Geometry will remain."
            )

        # If all passes
        else:
            # Check if we have a current state already.
            state = self._state()
            # Initialise the model
            model = FluxBasedModel(
                state,
                mb_model=self.mass_balance,
                y0=self.age,
                glen_a=self.creep,
                fs=self.basal_sliding,
            )
            # Run the model. Store the history.
            try:
                out = model.run_until_and_store(year, fl_diag_path=None)
            # If it fails, see above.
            except RuntimeError:
                print("Glacier grew out of its domain, stepping back five years")
                # Ohhh recursion
                self.progress_to_year(year - 5)
                return

            # Update attributes.
            self.history = out[0]
            self.state_history = out[1][0]
            self._current_state = model.fls[0]
            self._model_state = model
            self.age = model.yr

    def progress_to_equilibrium(self, years=2500, t_rate=0.0001):
        """Progress the glacier to equilibrium.

        Parameters
        ----------
        years : int, optional
            Specify the number of years during which we try to find
            an equilibrium state.
        t_rate : float, optional
            Specify how slow the glacier is allowed to change without
            reaching equilibrium.
        """

        def stop_function(model, previous_state):
            """Function to stop the simulation when equilbrium is
            reached. Basically a re-shape of the criterium of
            run_until_equilibrium."""
            # We don't stop unless
            stop = False
            # Ambigous rate, basically how fast is the glacier
            # changing every step.
            rate = t_rate
            # How many times to we try
            max_ite = years
            # If we have a previous step check it
            if previous_state is not None:
                # Here we save some stuff to diagnose the eq. state
                # If this is true, we update the state:
                if (
                    (previous_state["t_rate"] > rate)
                    and (previous_state["ite"] <= max_ite)
                    and (previous_state["was_close_zero"] < 5)
                ):

                    # Increase iterations.
                    previous_state["ite"] += 1
                    # Get the current volume
                    v_af = model.volume_m3
                    # If volume before is close to zero, update counter.
                    if np.isclose(previous_state["v_bef"], 0, atol=1):
                        previous_state["was_close_zero"] += 1
                        previous_state["t_rate"] = 1
                    # If not close to zero, update how slow volume is updating.
                    else:
                        previous_state["t_rate"] = (
                            np.abs(v_af - previous_state["v_bef"])
                            / previous_state["v_bef"]
                        )
                    previous_state["v_bef"] = v_af
                # If we go over the iteration limit.
                elif previous_state["ite"] > max_ite:
                    # raise RuntimeError('Not able to find equilbrium')
                    print(f"Not able to find equilibrium within {years} years")
                    stop = True
                # Otherwise we stop.
                else:
                    stop = True

            # If we don't have a previous state, define it.
            else:
                # Dictionary containing the stuff we need.
                previous_state = {
                    "ite": 0,
                    "was_close_zero": 0,
                    "t_rate": 1,
                    "v_bef": model.volume_m3,
                }

            return stop, previous_state

        # Do we have a future temperature changes assigned?
        if self.age < self.mass_balance._temp_bias_series.year.iloc[-1]:
            # If so, progress normally until finished.
            self.progress_to_year(self.mass_balance._temp_bias_series.year.iloc[-1])
        # Then we can find the eq. state.
        # Initialise the model
        state = self._state()
        model = FluxBasedModel(
            state,
            mb_model=self.mass_balance,
            y0=self.age,
            glen_a=self.creep,
            fs=self.basal_sliding,
        )
        # Run the model.
        try:
            #  Run with a stopping criteria.
            out = model.run_until_and_store(
                years, fl_diag_path=None, stop_criterion=stop_function
            )

        except RuntimeError:
            # We chose to print and return instead of raising since the
            # collection will then be able to continue.
            print(
                "Glacier grew out of its domain before reaching an equilibrium state."
            )
            return

        # Update attributes.
        self.history = out[0]
        self.state_history = out[1][0]
        self._current_state = model.fls[0]
        self.age = model.yr
        self._model_state = model
        # Remember the eq. year
        self._eq_states[self.age] = self.mass_balance.ela_h

    @edu_plotter
    def plot(self):
        """Plot the current state of the glacier."""
        _, ax1, ax2 = self.bed._create_base_plot()

        # If we have a current state, plot it.
        if self.current_state is not None:
            # Some masking shenanigans
            diff = self.current_state.surface_h - self.bed.bed_h
            mask = diff > 0
            idx = diff.argmin()
            mask[: idx + 1] = True
            # Fill the glacier.
            ax1.fill_between(
                self.bed.distance_along_glacier,
                self.bed.bed_h,
                self.current_state.surface_h,
                where=mask,
                color="white",
                lw=2,
            )
            # Add outline
            ax1.plot(
                self.bed.distance_along_glacier[mask],
                self.current_state.surface_h[mask],
                lw=2,
                label="Current glacier outline",
            )
            # Fill in the glacier in the topdown view.
            # Where does the glacier have thickness?
            filled = np.where(self.current_state.thick > 0, self.bed.widths, 0)
            # Fill vetween them
            ax2.fill_between(
                self.bed.distance_along_glacier,
                -filled / 2 * self.bed.map_dx,
                filled / 2 * self.bed.map_dx,
                where=filled > 0,
                color="white",
                edgecolor="C0",
                lw=2,
            )
            ax1.set_ylim((self.bed.bottom, self.current_state.surface_h[0] + 200))

        # ELA
        if self.ela is not None:
            ax1.axhline(self.ela, ls="--", c="k", lw=1)
            ax1.text(
                self.bed.distance_along_glacier[-1],
                self.ela + 10,
                "ELA",
                horizontalalignment="right",
                verticalalignment="bottom",
            )
            # Where along the bed is the ELA? Convert height to
            # distance along glacier kind of.
            if self.current_state is not None:
                idx = (np.abs(self.current_state.surface_h - self.ela)).argmin()
                # Plot the ELA in top down
                ax2.vlines(
                    self.bed.distance_along_glacier[idx],
                    ymin=-self.bed.widths[idx] / 2 * self.bed.map_dx,
                    ymax=self.bed.widths[idx] / 2 * self.bed.map_dx,
                    color="k",
                    ls="--",
                    lw=1,
                )
            # If we don't have a state yet, plot the ELA on the bed.
            else:
                # Where is the ela in regards to the bed height?
                idx = (np.abs(self.bed.bed_h - self.ela)).argmin()
                # Add vertical line.
                ax2.vlines(
                    self.bed.distance_along_glacier[idx],
                    ymin=-self.bed.widths[idx] / 2 * self.bed.map_dx,
                    ymax=self.bed.widths[idx] / 2 * self.bed.map_dx,
                    color="k",
                    ls="--",
                    lw=1,
                )

        # Decorations
        ax1.set_title(f"Glacier state at year {int(self.age)}")
        ax1.legend(loc="lower left")
        ax2.set_xlabel("Distance along glacier [km]")

    @edu_plotter
    def plot_mass_balance(self):
        """Plot the mass balance profile of the glacier."""
        plt.plot(
            self.annual_mass_balance,
            self.bed.bed_h,
            label="Mass balance",
            c="tab:orange",
        )
        plt.xlabel("Annual mass balance [m yr-1]")
        plt.ylabel("Altitude [m]")

        # Add ELA and 0 lines.
        plt.axvline(x=0, ls="--", lw=0.8, label="Mass balance = 0", c="tab:green")
        plt.axhline(y=self.ela, ls="--", lw=0.8, label="ELA", c="tab:blue")
        plt.title("Mass balance profile")
        plt.legend()

    @edu_plotter
    def _create_history_plot_components(
        self, show_bias=False, window=None, time_range=None, invert=False
    ):
        """Create components for the history plot of the glacier."""

        if show_bias:
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=4, sharex=True)
        else:
            fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

        # First point to all data.
        data = self.history
        bias_series = self.mass_balance.temp_bias_series
        # If the user supplied a time_range.
        if isinstance(time_range, Sequence):
            if time_range[0] >= self.age:
                raise ValueError(
                    "Lower end of time_range should be before age of glacier."
                )
            # Select data from time range only.
            data = self.history.sel(time=slice(time_range[0], time_range[1]))
            bias_series = bias_series.loc[
                (bias_series["year"] >= time_range[0])
                & (bias_series["year"] <= time_range[1])
            ]

        # Plot the length, volume and area if we have a history.
        if self.history is not None:
            data.length_m.plot(ax=ax1)
            data.volume_m3.plot(ax=ax2)
            data.area_m2.plot(ax=ax3)
        # If not, we print a message along with the empty plot.
        else:
            print("Glacier has no history yet, try progressing the glacier.")
        # Labels and such.
        ax1.set_xlabel("")
        ax1.set_title(f"Glacier history at year {int(self.age)}")
        ax1.annotate(
            "Glacier length",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax1.set_ylabel("Length [m]")
        # Volume labels.
        ax2.set_xlabel("")
        ax2.annotate(
            "Glacier volume",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax2.set_ylabel("Volume [m$^3$]")
        # Area labels.
        ax3.set_xlabel("Year")
        ax3.annotate(
            "Glacier area",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax3.set_ylabel("Area [m$^2$]")

        # Grid
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)

        if show_bias and self.history:
            window_str = ""
            if window:
                bias_series.bias.rolling(
                    window, min_periods=0, center=True
                ).mean().plot(ax=ax4)
                window_str = f", {window} yr. mean"
            else:
                bias_series.bias.plot(ax=ax4)
            ax4.grid(True)
            ax4.set_xlabel("Year")
            ax4.set_ylabel("Bias [°C]")

            ax4.annotate(
                "Temperature bias" + window_str,
                (0.98, 0.1),
                xycoords="axes fraction",
                bbox={"boxstyle": "Round", "color": "lightgrey"},
                ha="right",
            )
            if invert:
                ax4.invert_yaxis()

            return fig, ax1, ax2, ax3, ax4

        return fig, ax1, ax2, ax3

    @edu_plotter
    def plot_history(self, show_bias=False, window=None, time_range=None, invert=False):
        """Plot the history of the glacier.

        Parameters
        ----------
        show_bias : bool, optional
            Add a fourth axis, showing the history of the temperature bias.
            False by default.
        window : int, optional
            Controls the size (year) of the rolling window used to smooth the
            temperature bias.
        time_range : array_like(int, int), optional
            Select a subset of the data to plot.
        invert : bool, optional
            Chose to invert the y-axis on the bias plot. False by default.
        """
        # Get the components
        if show_bias:
            fig, ax1, ax2, ax3, ax4 = self._create_history_plot_components(
                show_bias=show_bias, window=window, time_range=time_range, invert=invert
            )
        else:
            fig, ax1, ax2, ax3 = self._create_history_plot_components(
                window=window, time_range=time_range
            )

    @edu_plotter
    def plot_state_history(self, interval=50, eq_states=False):
        """Plot the state history of the glacier (thicknesses) at specified
        intervals.

        Parameters
        ----------
        interval : int
            Specifies the number of years between each state in the plot.
        eq_states : bool
            Plot the different equilibrium states, if there are any. This takes
            precedence over the intervals.
        """
        # Get the base plotting components from the bed.
        _, ax1, ax2 = self.bed._create_base_plot()

        # We need a manual color cycle for the top down view.
        prop_cycle = plt.rcParams["axes.prop_cycle"]
        colors = cycle(prop_cycle.by_key()["color"])

        # Do we have any states?
        if not self.state_history:
            print(
                "Glacier doesn't have a state history yet, try progressing the glacier."
            )
            # We don't want to do anything else, since some operation depend on the state_history.
            return
        # If we don't want eq. states.
        elif not eq_states:
            # Want to plot thickness at specified intervals. So we slice it.
            states = self.state_history.thickness_m.isel(
                time=slice(interval, -1, interval)
            )
            # Length of state. Needed for sorting.
            len_states = self.history.length_m.isel(time=slice(interval, -1, interval))
            # Title
            title = "Glacier states"
        # If we wan't eq. states
        else:
            if self.eq_states:
                # Get the states.
                years = list(self.eq_states)
                states = self.state_history.thickness_m.sel(time=years)
                # Length of state. Needed for sorting.
                len_states = self.history.length_m.sel(time=years)
                # Title
                title = "Glacier equilibirum states"
            else:
                print("No equilbrium states to plot yet.")
                return

        sorted_index = np.argsort(len_states.values)
        # Sort the states by length and plot it in reverse.
        # I.e. plot the longest state first.
        states = states.values[sorted_index][::-1]
        # Loop over states.
        for i, state in zip(sorted_index[::-1], states):
            # Some masking shenanigans
            mask = state > 0
            idx = state.argmin()
            mask[: idx + 1] = True
            # Fill the glacier.
            ax1.fill_between(
                self.bed.distance_along_glacier,
                self.bed.bed_h,
                state + self.bed.bed_h,
                where=mask,
                color="white",
                lw=2,
            )
            # Label for outline
            if not eq_states:
                label = interval + i * interval
            else:
                label = list(self.eq_states)[i]
                ela = self.eq_states[label]

                # Add hline for ELAS
                ax1.axhline(ela, ls=":")
                ax1.text(
                    self.bed.distance_along_glacier[-1] - 0.2,
                    ela + 5,
                    f"ELA at year {label}",
                    ha="right",
                )
            # Add outline
            # Modify the zorder to get lines to show up nice.
            ax1.plot(
                self.bed.distance_along_glacier[mask],
                state[mask] + self.bed.bed_h[mask],
                lw=2,
                label=f"Glacier outline at year {label}",
                # zorder=4+i*0.1
            )
            # Fill in the glacier in the topdown view.
            # Where does the glacier have thickness?
            filled = np.where(state > 0, self.bed.widths, 0)
            # Fill vetween them
            # Modify the zorder to get lines to show up nice.
            ax2.fill_between(
                self.bed.distance_along_glacier,
                -filled / 2 * self.bed.map_dx,
                filled / 2 * self.bed.map_dx,
                where=filled > 0,
                facecolor="white",
                edgecolor=next(colors),
                lw=2,
                # zorder=1+i*0.1
            )
        # New title.
        ax1.set_title(title)
        # Nat. sort. Thanks stackoverflow.
        ax1.legend(
            *zip(
                *sorted(
                    zip(*ax1.get_legend_handles_labels()),
                    key=lambda s: [
                        int(t) if t.isdigit() else t.lower()
                        for t in re.split(r"(\d+)", s[1])
                    ],
                )
            )
        )


class SurgingGlacier(Glacier):
    """A surging glacier. This will have the same attributes as a normal
    glacier but with some extensions e.g. normal years and surging years.
    """

    def __init__(self, bed=None, mass_balance=None):
        """Initialise the surging glacier. Inherit attributes and methods
        from the Glacier class and extend it with some attributes specific
        for surging glaciers.
        """

        # Inherit from glacier
        super().__init__(bed, mass_balance)

        # Surging attributes
        self._normal_years = 50
        self._surging_years = 5
        # Basal sliding during surge has a sane default.
        # So no need to touch it.
        self._basal_sliding_surge = 5.7e-20 * 10
        self._basal_sliding = 5.7e-20
        # Some state attributes used by the progress method
        # to determine if we are surging or normal
        self._normal_period = True
        self._normal_years_left = self.normal_years
        self._surging_years_left = self.surging_years

    def _to_json(self):
        """Json represenation"""
        state = self._state()
        json = {
            "Type": type(self).__name__,
            "Age": int(self.age),
            "Length [m]": state.length_m,
            "Area [km2]": state.area_km2,
            "Volume [km3]": state.volume_km3,
            "Max ice thickness [m]": state.thick.max(),
            "Surging periodicity (off/on)": [[self.normal_years, self.surging_years]],
            "Surging now?": not self._normal_period,
        }
        return json

    def reset(self):
        """Reset the state of the surging glacier."""
        # Extend from glacier.
        super(SurgingGlacier, self).reset()
        # Surging attributes
        self._normal_years = 50
        self._surging_years = 5
        # Basal sliding during surge has a sane default.
        # So no need to touch it.
        self._basal_sliding_surge = 5.7e-20 * 10
        self._basal_sliding = 5.7e-20
        # Some state attributes used by the progress method
        # to determine if we are surging or normal
        self._normal_period = True
        self._normal_years_left = self.normal_years
        self._surging_years_left = self.surging_years

    @property
    def normal_years(self):
        """Number of years that the glacier progress without surging."""
        return self._normal_years

    @normal_years.setter
    def normal_years(self, value):
        """Set the length of the normal period.

        Parameters
        ----------
        value : int
            Length of the normal period.
        """
        if value > 0 and isinstance(value, int):
            self._normal_years = value
            self._normal_years_left = value
        else:
            raise ValueError(
                "Normal years should be above 0 and and of the type integer."
            )

    @property
    def surging_years(self):
        """Number of years that the glacier progress during surges."""
        return self._surging_years

    @surging_years.setter
    def surging_years(self, value):
        """Set the length of the surging period.

        Parameters
        ----------
        value : int
            Length of surging period.
        """
        if value > 0 and isinstance(value, int):
            self._surging_years = value
            self._surging_years_left = value
        else:
            raise ValueError(
                "Surging years should be above 0 and and of the type integer."
            )

    @property
    def basal_sliding_surge(self):
        return self._basal_sliding_surge

    @basal_sliding_surge.setter
    def basal_sliding_surge(self, value):
        self._basal_sliding_surge = value

    def progress_to_year(self, year):
        """Progress the surging glacier to specified year.
        This will progress the glacier in periods of surging
        and not surging, specified by the `normal_years` and
        `surging_years` attributes.

        Parameters
        ----------
        year : int
            Which year to progress the surging glacier.
        """

        # Check if the glacier has a masss balance model
        if not self.mass_balance:
            string = (
                "To evolve the glacier it needs a mass balance."
                + "\nMake sure the ELA and mass balance gradient"
                + " are defined."
            )
            raise NotImplementedError(string)

        # Some checks on the year.
        elif year < 0:
            raise ValueError("Year has to be above zero")

        elif year <= self.age:
            warnings.warn(
                "Year has to be above the current age of"
                + " the glacier. It is not possible to"
                + " de-age the glacier."
                + " Geometry will remain."
            )

        # If all passes
        else:
            # How many years to have left to simulate
            years_left = year - self.age
            # While we have years to run we do the following...
            while years_left:
                # Check if we have a current state already.
                state = self._state()
                # If in a normal period
                if self._normal_period:
                    # How many years should we run?
                    # We either run for the normal period amount of
                    # yeasrs. Or for the years left we have left.
                    # or the normal years left from a previous run.
                    years_to_run = np.min(
                        [
                            years_left,
                            self.normal_years,
                            self._normal_years_left,
                        ]
                    )
                    # Cast to int
                    years_to_run = int(years_to_run + self.age)
                    # Update normal_years_left
                    self._normal_years_left -= years_to_run - self.age
                    # If we have no normal years left we change state.
                    if self._normal_years_left == 0:
                        # Re-set it
                        self._normal_years_left = self.normal_years
                        # Not normal anymore
                        self._normal_period = not self._normal_period

                    # Initialise the model, width the normal basal_slidng
                    model = FluxBasedModel(
                        state,
                        mb_model=self.mass_balance,
                        y0=self.age,
                        glen_a=self.creep,
                        fs=self.basal_sliding,
                    )
                    # Run the model. Store the history.
                    try:
                        out = model.run_until_and_store(years_to_run, fl_diag_path=None)
                    except RuntimeError:
                        print("Glacier outgrew its domain and had to stop.")
                        # We should break here.
                        break

                # If we are not in normal state, we do a surging period.
                else:
                    # How many years should we run?
                    # Same as above but now we run for surging period amount
                    # of years.
                    years_to_run = np.min(
                        [
                            years_left,
                            self.surging_years,
                            self._surging_years_left,
                        ]
                    )
                    # Cast to int
                    years_to_run = int(years_to_run + self.age)
                    #  Update surging years left
                    self._surging_years_left -= years_to_run - self.age
                    # If there are no surging years left, we change state
                    if self._surging_years_left == 0:
                        # Re-set
                        self._surging_years_left = self.surging_years
                        # Not surging anymore
                        self._normal_period = not self._normal_period

                    # Initialise the model, with the surging basal_sliding
                    model = FluxBasedModel(
                        state,
                        mb_model=self.mass_balance,
                        y0=self.age,
                        glen_a=self.creep,
                        fs=self.basal_sliding_surge,
                    )
                    # Run the model. Store the history.
                    try:
                        out = model.run_until_and_store(years_to_run, fl_diag_path=None)
                    except RuntimeError:
                        print("Glacier outgrew its domain and had to stop.")
                        # We should break here.
                        break

                # Update attributes.
                self.history = out[0]
                self.state_history = out[1][0]
                self._current_state = model.fls[0]
                self._model_state = model
                self.age = model.yr
                # Check where we are
                years_left = year - self.age

    def progress_to_equilibrium(self):
        """Surging glaciers do not really have an eq. state."""
        raise NotImplementedError(
            "Surging glaciers do not progress to equilibrium. Yet..."
        )

    @edu_plotter
    def plot_history(self):
        """Plot the history of the surging glacier.
        Extends the Glacier.plot_history() method."""
        # Get the base plotting components.
        fig, ax1, ax2, ax3 = self._create_history_plot_components()

        # We then want to add markers for the surging years.
        # How many surges do we have?
        nr_surges = int(self.age / (self.normal_years + self.surging_years))
        # Loop over the surges
        for i in range(nr_surges):
            # When should the span start
            start = (i + 1) * self.normal_years + i * self.surging_years
            # and end.
            end = (
                (i + 1) * self.normal_years
                + self.surging_years
                + i * self.surging_years
            )
            # Add spans
            ax1.axvspan(start, end, color="tab:orange", alpha=0.3)
            ax2.axvspan(start, end, color="tab:orange", alpha=0.3)
            ax3.axvspan(start, end, color="tab:orange", alpha=0.3)

        # Legend entry
        patch = Patch(facecolor="tab:orange", alpha=0.3, label="Surging period")
        fig.legend(handles=[patch], loc="upper left", bbox_to_anchor=(0.9, 0.89))
