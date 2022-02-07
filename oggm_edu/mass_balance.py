"""This module contains the MassBalance class, an abstract interface to
the OGGM mass balance model which is to be used with the Glacier and
SurgingGlacier classes.
"""

# Other libraries.
import pandas as pd

# Import OGGM things.
from oggm.core.massbalance import LinearMassBalance, ScalarMassBalance


class MassBalance(LinearMassBalance):
    """Mass balance class"""

    def __init__(self, ela, gradient, hemisphere=None, density=None):
        """Initialise the mass balance from the ELA and the gradient.

        Parameters
        ----------
        ela : int or float
            Equilibrium line altitude of the mass balance. Units: m.
        gradient : int or float
            Mass balance gradient. Define the altitude relation of the mass balance.
        """
        super().__init__(ela_h=ela, grad=gradient)

        # Temperature bias evolution
        self._temp_bias_final = 0.0
        self._temp_bias_grad = 0.0
        self._temp_bias_intersect = 0.0
        self._temp_bias_final_year = 0

    def _to_json(self):
        json = {
            "ELA [m]": self.ela_h,
            "Original ELA [m]": self.orig_ela_h,
            "Temperature bias [C]": self.temp_bias,
            "Gradient [mm/m/yr]": self.grad,
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

    @property
    def gradient(self):
        return self.grad

    @gradient.setter
    def gradient(self, value):
        """Define the mass balance gradient.

        Parameters
        ----------
        value : int or float
            Mass balance altitude gradient, mm/m.
        """
        # We cant have a negative gradient.
        if value > 0:
            self.grad = value
        else:
            raise ValueError("Mass balance gradient less than 0 not allowed")

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
        # Check that criteria are met.
        if isinstance(temp_bias, float) and isinstance(duration, int):
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
