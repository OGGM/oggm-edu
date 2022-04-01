"""This module contains the MassBalance class, an abstract interface to
the OGGM mass balance model which is to be used with the Glacier and
SurgingGlacier classes.
"""

# Other libraries.
import numpy as np
import pandas as pd
from collections.abc import Sequence

# Import OGGM things.
from oggm.core.massbalance import MassBalanceModel, ScalarMassBalance
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
        self._temp_bias_final = 0.0
        self._temp_bias_grad = 0.0
        self._temp_bias_intersect = 0.0
        self._temp_bias_final_year = 0

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
        self._temp_bias_final = 0.0
        self._temp_bias_grad = 0.0
        self._temp_bias_intersect = 0.0
        self._temp_bias_final_year = 0

    @property
    def gradient(self):
        return self.grad

    # TODO create a gradient setter where we can also change complex gradients after init.
    @gradient.setter
    def gradient(self, value):
        """Define the mass balance gradient. Only work for setting simple gradients.

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

    def get_monthly_mb(self, heights, **kwargs):
        """Calculate the monthly mass balance for the glacier."""

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

    def get_annual_mb(self, heights, **kwargs):
        """Get the annual mass balance."""
        return self.get_monthly_mb(heights, **kwargs)

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
        """Current temperature bias applied to the mass balance. Unit: °C"""
        return self._temp_bias

    @temp_bias.setter
    def temp_bias(self, value):
        """Add temperature bias, and update ELA."""
        self.ela_h = self.orig_ela_h + value * 150
        self._temp_bias = value

    def _update_temp_bias(self, year):
        """Updates the temperature bias internally during progression."""
        # Change the temperature bias
        new_temp_bias = self._temp_bias_grad * year + self._temp_bias_intersect
        self.temp_bias = new_temp_bias

    def _add_temp_bias(self, temp_bias, duration, year):
        """Method to add a gradual temperature bias to the mass balance of the
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
        # Check that we don't have a temperature bias scenario already.
        if self._temp_bias_final_year != 0 and year <= self._temp_bias_final_year:
            raise RuntimeError(
                "We can't add a new temperature bias while the previous one is\nstill being evaluated."
            )
        # Check that criteria are met.
        elif isinstance(temp_bias, float) and isinstance(duration, int):
            # Set the temperature bias.
            self._temp_bias_final = temp_bias
            # Set the final year
            self._temp_bias_final_year = year + duration
            # Calculate the gradient, linear for now.
            self._temp_bias_grad = (self._temp_bias_final - self.temp_bias) / duration
            # And the intersect
            self._temp_bias_intersect = self._temp_bias_final - (
                self._temp_bias_grad * self._temp_bias_final_year
            )

        else:
            raise TypeError("Temperature bias and/or duration of wrong type")


class ZeroMassBalance(ScalarMassBalance, MassBalance):
    # TODO: yeah this is crap lets discuss in the PR
    pass
