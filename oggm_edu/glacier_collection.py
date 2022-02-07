"""This module provides a utility class, GlacierCollection, designed to ease
the handling of multiple glaciers.
"""

# Internals
from oggm_edu.glacier import Glacier
from oggm_edu.funcs import edu_plotter

# Other libraries.
import pandas as pd
import numpy as np
import collections

# Plotting
from matplotlib import pyplot as plt


class GlacierCollection:
    """This is class for storing multiple glaciers, providing convenient
    methods for comparing them.
    """

    def __init__(self, glacier_list=None):
        """Initialise the glacier collection.

        Parameters
        ----------
        glacier_list : list of glaciers objects
            Defaults to none. Has the possibility to add glaciers on the go.
        """

        self._glaciers = []

        # Do we have a list of glaciers?
        if glacier_list:
            # Check that all are Glaciers.
            if all(isinstance(glacier, Glacier) for glacier in glacier_list):
                self._glaciers = glacier_list

    def __repr__(self):
        return f"Glacier collection with {len(self._glaciers)} glaciers."

    def _repr_html_(self):
        # Pretty representation for notebooks.
        # Get the first glacier and base the creation of the dataframe of this.
        # If we have glaciers in the collection.
        if len(self._glaciers) > 0:
            json = {
                **self._glaciers[0]._to_json(),
                **self._glaciers[0].bed._to_json(),
                **self._glaciers[0].mass_balance._to_json(),
            }
            # Create the dataframe.
            df = pd.DataFrame(json, index=[0])
            # We then loop over the rest of the collection.
            for glacier in self._glaciers[1:]:
                # Next json representation
                json = {
                    **glacier._to_json(),
                    **glacier.bed._to_json(),
                    **glacier.mass_balance._to_json(),
                }
                # Add it to the df.
                df2 = pd.DataFrame(json)
                df = pd.concat([df, df2], ignore_index=True)
            df.index.name = "Glacier"
            # Return the html representation of the dataframe.
            return df._repr_html_()
        # If empty.
        else:
            pass

    def check_collection(self, glacier):
        """Utility method. Check if the glaciers obey the collection rules.
        They need to have the same domains for this to make sense I think."""
        # TODO

    @property
    def glaciers(self):
        return self._glaciers

    @property
    def annual_mass_balance(self):
        return [glacier.annual_mass_balance for glacier in self.glaciers]

    def fill(self, glacier, n, attributes_to_change=None):
        """Fill the collection with a desired number of glaciers.

        Parameters
        ----------
        glacier : Glacier
            Initial glacier, to base the rest of the collection on.
        n : int
            Specify number of glaciers in the collection.
        attributes_to_change : dict
            Dictionary where key value pairs correspond to the
            attribute and values to be assigned each glacier.
            See GlacierCollection.change_attributes for more.
        """
        # Is original a valid glacier?
        if not isinstance(glacier, Glacier):
            raise TypeError("Glacier collection can only contain glacier objects.")
        # Check n.
        elif not isinstance(n, int):
            raise TypeError("n should be an integer.")

        else:
            # The bread and butter of the function,
            # Fill the collection.
            for _ in range(n):
                # Add a copy of the glacier.
                self.add(glacier.copy())

        # Do we change some vars?
        if attributes_to_change:
            self.change_attributes(attributes_to_change)

    def add(self, glacier):
        """Add one or more glaciers to the collection.

        Parameters
        ----------
        glacier : oggm.edu Glacier object or array_like with
        Glacier objects
        """
        # Check if iterable
        if isinstance(glacier, collections.Sequence):
            for glacier in glacier:
                # Check that glacier is of the right type.
                if not isinstance(glacier, Glacier):
                    raise TypeError(
                        "Glacier collection can only contain glacier objects."
                    )
                # Is the glacier already in the collection?
                if glacier in self._glaciers:
                    raise AttributeError("Glacier is already in collection")
                # If the glacier is an instance of Glacier, we can add it to
                # the collection.
                else:
                    self._glaciers.append(glacier)
        # If not iterable
        else:
            # Check that glacier is of the right type.
            if not isinstance(glacier, Glacier):
                raise TypeError("Glacier collection can only contain glacier objects.")
            # Is the glacier already in the collection?
            if glacier in self._glaciers:
                raise AttributeError("Glacier is already in collection")
            # If the glacier is an instance of Glacier, we can add it to
            # the collection.
            else:
                self._glaciers.append(glacier)

    def change_attributes(self, attributes_to_change):
        """Change the attribute(s) of the glaciers in the collection.

        Parameters
        __________
        attributes_to_change : dict
            Dictionary where the key value pairs follow the structure:
            {'key': [n values], ...}, where 'key' match an attribute
            of the glacier and n match the length of the collection.
            Valid values for key are:
            - gradient
            - ela
            - basal_sliding
            - creep
            - normal_years
            - surging_years
            - basal_sliding_surge
        """
        # Did we get a dict?
        if not isinstance(attributes_to_change, dict):
            raise TypeError("attributes_to_change should be a dictionary.")

        # What are we allowed to change??
        valid_attrs = (
            "gradient",
            "ela",
            "basal_sliding",
            "creep",
            "normal_years",
            "surging_years",
            "basal_sliding_surge",
        )
        mb_attrs = ("gradient", "ela")
        # For each key-value pair:
        for key, values in attributes_to_change.items():
            # Is current key valid?
            if key not in valid_attrs:
                raise ValueError(f"Attribute {key} not a valid attribute for function.")
            # Are the value valid?
            elif not isinstance(values, collections.Sequence):
                raise TypeError("Provided value should be in the form of a list/tuple")
            elif not len(values) == len(self.glaciers):
                raise ValueError(
                    "Numbers of values provided does not match size of collection."
                )
            # If all passes
            else:
                for (glacier, value) in zip(self.glaciers, values):
                    # Use built in setattr. Should respect the defined
                    # setters, with error messages an such.
                    if key in mb_attrs:
                        setattr(glacier.mass_balance, key, value)
                    else:
                        setattr(glacier, key, value)

    def progress_to_year(self, year):
        """Progress the glaciers within the collection to
        the specified year.

        Parameters
        ----------
        year : int
            Which year to grow the glaciers.
        """
        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")

        # Loop over the glaciers within the collection.
        for glacier in self._glaciers:
            glacier.progress_to_year(year)

    def progress_to_equilibrium(self, years=2500, t_rate=0.0001):
        """Progress the glaciers to equilibrium.

        Parameters
        ----------
        years : int, optional
            Specify the number of years during which we try to find
            an equilibrium state.
        t_rate : float, optional
            Specify how slow the glacier is allowed to change without
            reaching equilibrium.
        """
        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")

        # Loop.
        for glacier in self._glaciers:
            glacier.progress_to_equilibrium(years=years, t_rate=t_rate)

    @edu_plotter
    def plot(self):
        """Plot the glaciers in the collection to compare them."""

        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")
        # We use this to plot the bedrock etc.
        gl1 = self._glaciers[0]
        # Get the ax from the first plot
        fig, ax = plt.subplots()
        # Bedrock
        ax.plot(
            gl1.bed.distance_along_glacier,
            gl1.bed.bed_h,
            label="Bedrock",
            ls=":",
            c="k",
            lw=2,
            zorder=3,
        )
        ax.set_ylim((gl1.bed.bottom, gl1.bed.top + 200))
        # Fill it in.
        ax.fill_betweenx(
            gl1.bed.bed_h, gl1.bed.distance_along_glacier, facecolor="lightgrey"
        )

        # Set the title.
        ax.set_title("Glacier collection")

        elas = []
        # Loop over the collection.
        for i, glacier in enumerate(self._glaciers):
            # Plot the surface
            if glacier.current_state is not None:
                # Masking shenanigans.
                diff = glacier.current_state.surface_h - glacier.bed.bed_h
                mask = diff > 0
                idx = diff.argmin()
                mask[: idx + 1] = True
                # Fill the ice.
                ax.fill_between(
                    glacier.bed.distance_along_glacier,
                    glacier.current_state.surface_h,
                    glacier.bed.bed_h,
                    where=mask,
                    facecolors="white",
                    # edgecolors=color_cycler(i),
                    # lw=2,
                )
                # Plot outline
                ax.plot(
                    glacier.bed.distance_along_glacier[mask],
                    glacier.current_state.surface_h[mask],
                    label=f"Glacier {i} at year" + f" {glacier.age}",
                )
                # Ylim
                ax.set_ylim((gl1.bed.bottom, gl1.current_state.surface_h[0] + 200))
            elas.append(glacier.ela)

        # If all elas are equal.
        if len(set(elas)) == 1:
            # Plot the ELA
            ax.axhline(elas[0], ls="--", zorder=1)
            ax.text(
                glacier.bed.distance_along_glacier[-1],
                elas[0] + 10,
                "All ELAs are equal",
                ha="right",
                va="bottom",
            )
        # If elas not equal.
        else:
            # Do we have some elas that are equal?
            # Get a set dictionary of ELAs.
            elas_d = {key: "" for key in set(elas)}
            # Fill it.
            for i, key in enumerate(elas):
                elas_d[key] += f"{i}, "

            # Loop the unique ELAs.
            for ela, string in elas_d.items():
                # Add the annotation.
                ax.text(
                    glacier.bed.distance_along_glacier[-1],
                    ela + 10,
                    f"ELA  glacier {string[:-2]}",
                    ha="right",
                    va="bottom",
                )
                # Plot the ELA
                ax.axhline(ela, ls="--", zorder=1)

        # axis labels.
        ax.set_xlabel("Distance along glacer [km]")
        ax.set_ylabel("Altitude [m]")
        ax.set_xlim((0, gl1.bed.distance_along_glacier[-1] + 2))
        ax.set_facecolor("#ADD8E6")
        plt.legend(loc="lower left")
        # Add a second legend with infos.
        # It would be cool to only show attributes that are different.
        labels = []
        for glacier in self._glaciers:
            # Create the label
            label = (
                f"ELA: {glacier.ela} \n"
                f"MB grad: {glacier.mb_gradient} \n"
                f"Age: {glacier.age} \n"
                f"Creep: {glacier.creep:.2e} \n"
                f"Sliding: {glacier.basal_sliding}"
            )
            # Append the label to the list.
            labels.append(label)
        # Get the handles back
        handles, _ = ax.get_legend_handles_labels()
        # Create the legend
        fig.legend(
            handles[1:],
            labels,
            title="Glacier info",
            loc="upper left",
            bbox_to_anchor=(0.9, 0.89),
        )

    @edu_plotter
    def plot_history(self):
        """Plot the histories of the collection"""

        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, sharex=True)

        # Check so that the glacier has a history.
        for i, glacier in enumerate(self._glaciers):
            if glacier.history is not None:
                # Plot the length.
                glacier.history.length_m.plot(ax=ax1)
                # Plot the volume
                glacier.history.volume_m3.plot(ax=ax2)
                # Plot the area
                glacier.history.area_m2.plot(
                    ax=ax3,
                    label=f"Glacier {i}\n"
                    + f"ELA: {glacier.ela}\n"
                    + f"MB grad: {glacier.mb_gradient}\n"
                    + f"Age: {glacier.age}\n"
                    + f"Creep: {glacier.creep:.2e}\n"
                    + f"Sliding: {glacier.basal_sliding}",
                )
            else:
                print("Glacier history missing")
        # Decorations
        ax1.set_xlabel("")
        ax1.set_title("Glacier collection evolution")
        ax1.annotate(
            "Glacier length",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax1.set_ylabel("Length [m]")
        ax2.set_xlabel("")
        ax2.annotate(
            "Glacier volume",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax2.set_ylabel("Volume [m$^3$]")
        ax3.set_xlabel("Year")
        ax3.annotate(
            "Glacier area",
            (0.98, 0.1),
            xycoords="axes fraction",
            bbox={"boxstyle": "Round", "color": "lightgrey"},
            ha="right",
        )
        ax3.set_ylabel("Area [m$^2$]")
        # Grid on.
        ax1.grid(True)
        ax2.grid(True)
        ax3.grid(True)

        handels, labels = ax3.get_legend_handles_labels()
        fig.legend(
            handels,
            labels,
            loc="upper left",
            ncol=1,
            title="Glacier info",
            bbox_to_anchor=(0.9, 0.89),
        )

    @edu_plotter
    def plot_mass_balance(self):
        """Plot the mass balance(s) for the glaciers in the collection"""

        fig, ax = plt.subplots()

        # How many unique ELAS do we have?
        elas = []

        # Plot annual mass balance for each glacier.
        for i, glacier in enumerate(self.glaciers):
            ax.plot(
                glacier.annual_mass_balance,
                glacier.bed.bed_h,
                label=f"Glacier {i}, " + f"gradient {glacier.mass_balance.gradient}",
            )
            # Add each ELA.
            elas.append(glacier.mass_balance.ela)
        # Add labels.
        ax.set_xlabel("Annual mass balance [m yr-1]")
        ax.set_ylabel("Altitude [m]")

        # Add 0 lines.
        ax.axvline(x=0, ls=":", label="Mass balance = 0", c="tab:green")

        # Plot the ELAs.
        # If all elas are equal.
        if len(set(elas)) == 1:
            # Plot the ELA
            ax.axhline(elas[0], ls="--", zorder=1)
            # Where to place the annotation?
            extent = np.array(self.annual_mass_balance).min()
            ax.text(extent, elas[0] + 2, "All ELAs are equal", ha="left", va="bottom")
        # If elas not equal.
        else:
            # Do we have some elas that are equal?
            # Get a set dictionary of ELAs.
            elas_d = {key: "" for key in set(elas)}
            # Fill it.
            for i, key in enumerate(elas):
                elas_d[key] += f"{i}, "

            # Loop the unique ELAs.
            for ela, string in elas_d.items():
                # Add the annotation.
                extent = np.array(self.annual_mass_balance).min()
                ax.text(
                    extent,
                    ela + 2,
                    f"ELA  glacier {string[:-2]}",
                    ha="left",
                    va="bottom",
                )
                # Plot the ELA
                ax.axhline(ela, ls="--", zorder=1)
        ax.set_title("Mass balance profiles")

        plt.legend()
