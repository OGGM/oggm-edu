"""This module contains the MassBalance class, an abstract interface to
the OGGM mass balance model which is to be used with the Glacier and
SurgingGlacier classes.
"""

# Other libraries.
import numpy as np
import pandas as pd
from collections.abc import Sequence

# Import OGGM things.
from oggm.core.massbalance import MassBalanceModel
from oggm.utils import clip_max
from oggm.cfg import SEC_IN_YEAR


class MassBalance(MassBalanceModel):
    """Oggm Edu mass balance, used to construct the ``oggm_edu.Glacier``. The mass balance can be
    constructed with either a single mass balance gradient  resulting in a linear mass balance,
    or with multiple gradients - resulting in a non-linear mass balance profile.

    Attributes
    ----------
    ela : int or float
        Current equilibrium line altitude of the mass balance profile. Unit: m.
    grad : int or float or list
        Gradient of the mass balance profile. Single scalar if linear or multiple scalars if non-linear.
        Unit: mm/m/yr
    orig_ela_h : int or float
        Original equilibrium line altitude of the mass balance profile. Unit: m.
    temp_bias : float
        Current temperature bias applied to the mass balance. Unit: C.

    """

    def __init__(
        self,
        ela,
        gradient,
        breakpoints=None,
        max_mb=None,
        hemisphere=None,
        density=None,
    ):
        """Initialise the mass balance from the ELA and the gradient. Optionally pass breakpoints
        in the case of multiple gradients.

        Parameters
        ----------
        ela : int or float
            Equilibrium line altitude of the mass balance. Units: m.
        gradient : int or float or array_like(int or float)
            Mass balance gradient. Define the altitude relation of the mass balance.
            If array like with int/float, a mass balance with multiple gradients will be
            initialised.
        breakpoints : array_like(int or float) (Optional)
            Specify the altitude breakpoints between mass balance gradients.
        """
        super().__init__()

        self.hemisphere = "nh"
        self.valid_bounds = [-1e4, 2e4]

        # Mass balance attributes
        if ela >= 0:
            self.orig_ela_h = ela
            self.ela_h = ela
        else:
            raise ValueError("ela should be above or equal to zero.")
        # Max mb
        self.max_mb = max_mb

        # Did we get multiple gradients and breakpoints?
        if isinstance(gradient, Sequence) and breakpoints:
            # Are breakpints of the right length?
            if not len(gradient) == len(breakpoints) + 1:
                raise ValueError(
                    "There should be one breakpoint specified for every two mass balance gradients."
                )
            elif np.any(np.asarray(gradient) <= 0) or np.any(
                np.asarray(breakpoints) < 0
            ):
                raise ValueError(
                    "Gradients and breakpoints have to be above, or equal to, 0."
                )
            else:
                self.grad = gradient
                self._breakpoints = breakpoints
        # If we get multiple gradients but no break points.
        elif isinstance(gradient, Sequence) and not breakpoints:
            raise ValueError(
                "If multiple gradients are passed, breakpoints are required."
            )
        # Breakpoint but single gradient.
        elif not isinstance(gradient, Sequence) and breakpoints:
            raise ValueError("For a single gradient no breakpoints are needed.")
        # If all else passes, we should have a single gradient.
        else:
            if gradient >= 0:
                self.grad = gradient
            else:
                raise ValueError("gradient should be above, or equal, to zero.")

        # Temperature bias evolution
        self._temp_bias = 0
        self._temp_bias_series = pd.DataFrame({"year": [0], "bias": [self.temp_bias]})

    def _to_json(self):
        json = {
            "ELA [m]": self.ela_h,
            "Original ELA [m]": self.orig_ela_h,
            "Temperature bias [C]": self.temp_bias,
            "Gradient [mm/m/yr]": [self.grad],
            "Hemisphere": self.hemisphere,
            "Ice density [kg/m3]": self.rho,
        }
        return json

    def __repr__(self):
        json = self._to_json()
        string = "Glacier mass balance \n"
        # Create a nice string
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

    def reset(self):
        """Reset the mass balance to initial state."""
        # ELA
        self.ela = self.orig_ela_h
        # Temperature bias evolution
        self._temp_bias = 0
        self._temp_bias_series = pd.DataFrame({"year": [0], "bias": [self.temp_bias]})

    @property
    def gradient(self):
        """Mass balance altitude gradient, mm/m. (only works for simple gradients)."""
        return self.grad

    # TODO create a gradient setter where we can also change complex gradients after init.
    @gradient.setter
    def gradient(self, value):
        """Define the mass balance gradient (only works for simple gradients).

        Parameters
        ----------
        value : int or float
            Mass balance altitude gradient, mm/m.
        """
        # We cant have a negative gradient.
        if isinstance(self.grad, Sequence):
            raise TypeError(
                "Cannot set a single gradient when mass balance was initialised with multiple gradients."
            )

        elif value < 0:
            raise ValueError("Mass balance gradient less than 0 not allowed")
        else:
            self.grad = value

    @property
    def ela(self):
        """Altitude of the equilibrium line altitude (m)."""
        return self.ela_h

    @ela.setter
    def ela(self, value):
        """Define the equilibrium line altitude.

        Parameters
        ----------
        value : int or float
            Altitude of the ELA.
        """
        # We cant have a negative ELA.
        if value > 0:
            self.ela_h = value
        else:
            raise ValueError("ELA below 0 not allowed.")

    def get_monthly_mb(self, heights, year=None, **kwargs):
        """Calculate the monthly mass balance for the glacier.

        Parameters
        ----------
        heights : np.ndarray
            altitudes at which to compute the MB
        year : float, optional
            The current hydrological year. Used to evaluate if mass balance model should be updated.

        Returns
        -------
        The monthly mass-balances for each height.
        """

        # A year will always be provided during a model run, the only time we do this evaluation.
        # In ohter cases i.e. plotting annual mb, we don't evaluate this.
        # We check if its a float instead of simply if year since this would miss the 0th year.
        if isinstance(year, float):
            # Since we are progressing the glacier we want the next year of the climate to update
            # the mass balance.
            year = year + 1
            # If we have a future climate scenario essentially.
            if year <= self._temp_bias_series.year.iloc[-1]:
                # We get a temp bias from the series, update the ela of our mb.
                # Uses the temp_bias setter.
                self.temp_bias = self.temp_bias_series.bias[
                    self.temp_bias_series.year == year
                ].values[0]
            # If there is no future climate scenario, we simply append the current bias to the history.
            # e.g. when climate remains constant.
            else:
                # Add the current temperature bias (unchanged) to the history.
                df = pd.DataFrame({"year": [year], "bias": [self.temp_bias]})
                self._temp_bias_series = pd.concat(
                    [self._temp_bias_series, df]
                ).reset_index(drop=True)

        # Compute the mb
        # We use the _gradient_lookup to get an array of gradients matching the length of heights.
        # _breakpoint_diff computes the mb difference at the breakpoint height for the two different
        # gradients. Used to adjust the intercept of the new gradient curve.
        mb = (np.asarray(heights) - self.ela_h) * self._gradient_lookup(
            heights
        ) + self._breakpoint_diff(heights)

        # Adjust intercept for the case when breakpoint is above ELA.
        # Essentially making sure that the mb profile is zero at the ELA.
        ela_idx = np.argmin(np.abs(np.asarray(heights) - self.ela_h))
        mb = mb - mb[ela_idx]
        # Should we cap the mb?
        if self.max_mb:
            clip_max(mb, self.max_mb, out=mb)

        return mb / SEC_IN_YEAR / self.rho

    def get_annual_mb(self, heights, year=None, **kwargs):
        """Get the annual mass balance.

        Parameters
        ----------
        heights : np.ndarray
            altitudes at which to compute the MB

        Returns
        -------
        the mass-balances (same size as heights)
        """
        return self.get_monthly_mb(heights, year)

    def _gradient_lookup(self, heights):
        """Compute the mass balance gradient for the given heights.

        Parameters
        ----------
        heights : array_like(float or int)
            Collection of heights for which to find the corresponding gradient.

        Returns
        -------
        gradients : array
            Array of length == len(heights), where value at position i hold the gradient
            corresponding to height at pos. i. E.g. [15, 15, 15, 7, 7, 5].

        """
        # How many gradients do we need?
        gradients = np.zeros(len(heights))
        # If we hace multiple gradients
        if isinstance(self.gradient, Sequence):
            # We start with a linear profile
            gradients[:] = self.gradient[0]
            # Then we want to change the profile, per breakpoint
            for breakpoint, grad in zip(self._breakpoints, self.gradient[1:]):
                # Get the breakpoint index
                idx = np.argmin(np.abs(np.asarray(heights) - breakpoint))
                # Semi-broadcast, set the new gradient from the breakpoint and down.
                gradients[idx:] = grad
        # Single gradient
        else:
            gradients[:] = self.grad

        return gradients

    def _breakpoint_diff(self, heights):
        """Calculate how much a new section of the mb curve has to be shifted at the gradient
        breakpoint for curves to match.

        Parameters
        ----------
        heights : array_like(float or int)
            Collection of heights for which to find the corresponding mb difference.

        Returns
        -------
        diff : array
            Array matching the length of heights with values to shift the mass balance.
        """

        # We begin with zero difference.
        diff = np.zeros(len(heights))

        # If we hace multiple gradients.
        if isinstance(self.gradient, Sequence):
            # We loop over the breakpoints again.
            for i, breakpoint in enumerate(self._breakpoints):
                # From where in the diff array do we add the diff?
                idx = np.argmin(np.abs(np.asarray(heights) - breakpoint))
                # The mass balance difference between two gradients at the break point.
                mb_diff = (breakpoint - self.ela_h) * (
                    self.gradient[i] - self.gradient[i + 1]
                )
                # Add the mb_diff from breakpoint and down.
                diff[idx:] += mb_diff

        # If we only have one gradient, return a 0 diff.
        else:
            pass

        return diff

    @property
    def temp_bias(self):
        """Current temperature bias applied to the mass balance (unit: °C)"""
        return self._temp_bias

    @temp_bias.setter
    def temp_bias(self, value):
        """Add temperature bias, and update ELA."""
        self.ela_h = self.orig_ela_h + value * 150
        self._temp_bias = value

    @property
    def temp_bias_series(self):
        """Dataframe of historical and possible future temperature biases of the glacier.
        The user can create their own bias series through a pandas data frame.

        Parameters
        ----------
        df : Pandas.DataFrame
            Custom dataframe for temperature bias series.
            This dataframe should have two columns: 'year' and 'bias'. 'year' should
            start at the year after the current year of the glacier and increase monotonically.
        """
        return self._temp_bias_series

    @temp_bias_series.setter
    def temp_bias_series(self, df):
        """Allow the user to set a custom bias series."""
        # Need to perform some checks to make sure that the series fits the glacier.

        if not isinstance(df, pd.DataFrame):
            raise TypeError("The temp_bias_series should be a Pandas dataframe.")
        elif not np.all(df.columns == ["year", "bias"]):
            raise ValueError(
                "The columns of the dataframe should be 'year' and 'bias'."
            )
        elif not df.year.iloc[0] == self.temp_bias_series.year.iloc[-1] + 1:
            raise ValueError(
                "User supplied series should start after the current year."
            )
        elif not np.all(
            np.equal(df.year, np.arange(df.year.iloc[0], df.year.iloc[-1] + 1))
        ):
            raise ValueError("'year' should increase monotonically.")
        elif not pd.api.types.is_float_dtype(df["bias"]):
            raise ValueError("'bias' dtype should be float.")
        # If this passes we can add it.
        else:
            # Concat to the old series.
            self._temp_bias_series = pd.concat(
                [self._temp_bias_series, df]
            ).reset_index(drop=True)

    def add_temp_bias(self, temp_bias, duration, year):
        """Add a gradual temperature bias to the mass balance of the
        glacier.

        Parameters
        ----------
        temp_bias : float
            Final temperature bias to apply after the specified duration
        duration : int
            Number of year during which to apply the temperature bias.
        year : int
            Current age of the glacier
        """
        # Check that criteria are met.
        if isinstance(temp_bias, float) and isinstance(duration, int):
            # Create dummy arrays for biases and years.
            # From current bias to the new one during the duration.
            # Have to add one year for linspace to include the last year.
            # At the same time we don't need the first year.
            temp_biases = np.linspace(self.temp_bias, temp_bias, duration + 1)[1:]
            # If we already have a future, we append the climate from this year.
            # Otherwise start from the current year.
            year = np.max([year, self._temp_bias_series.year.iloc[-1]])
            # Years from next year to next + duration.
            years = np.arange(float(year + 1), float(year + duration + 1))

            # Then we create a df.
            df = pd.DataFrame({"year": years, "bias": temp_biases})

            # Add the new bias series to the one we already have.
            self._temp_bias_series = pd.concat(
                [self._temp_bias_series, df]
            ).reset_index(drop=True)

        else:
            raise TypeError("Temperature bias and/or duration of wrong type")

    def add_random_climate(self, duration, temperature_range, year):
        """Append a random climate to future of the mass balance of the glacier.

        Parameters
        ----------
        duration : int
            How many years should the random climate be.
        temperature_range : array_like(float, float)
            The range over which the climate should vary randomly.
        year : int
            Current age of the glacier.
        """

        # Check arges
        if not isinstance(int(duration), int):
            raise TypeError("duration should be the type integer.")
        elif not isinstance(temperature_range, Sequence) or len(temperature_range) != 2:
            raise TypeError("temp_range should be a sequence of two floats.")
        elif temperature_range[0] >= temperature_range[1]:
            raise ValueError(
                "Entries in temperature_range should be in increasing order."
            )
        else:
            # Create a random array of selected length.
            random_vals = np.random.rand(duration)
            # Transform to the selected range.
            random_temp_biases = (
                (temperature_range[1] - temperature_range[0]) * random_vals
            ) + temperature_range[0]

            # If we already have a future, we append the climate from this year.
            # Otherwise start from the current year.
            year = np.max([year, self._temp_bias_series.year.iloc[-1]])
            # Need some years.
            years = np.arange(float(year + 1), float(year + duration + 1))

            # Then we create a df.
            df = pd.DataFrame({"year": years, "bias": random_temp_biases})
            # And add it to the series.
            self._temp_bias_series = pd.concat(
                [self._temp_bias_series, df]
            ).reset_index(drop=True)
