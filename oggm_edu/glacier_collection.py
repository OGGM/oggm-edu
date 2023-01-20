"""This module provides a utility class, GlacierCollection, designed to ease
the handling of multiple glaciers.
"""

# Internals
from oggm_edu.glacier import Glacier
from oggm_edu.funcs import edu_plotter, expression_parser

# Other libraries.
import pandas as pd
import numpy as np
from collections.abc import Sequence
from multiprocessing import Pool
from functools import partial

# Plotting
from matplotlib import pyplot as plt


class GlacierCollection:
    """This is an object used to store multiple glaciers.

    It provides methods to progress and compare the glaciers in the collection.
    """

    def __init__(self, glacier_list=None):
        """Initialise the glacier collection.

        Parameters
        ----------
        glacier_list : list of glaciers objects
            Defaults to none. Has the possibility to add glaciers on the go.
            Glaciers need to have the same bed slope.
        """

        self._glaciers = []

        # Do we have a list of glaciers?
        if glacier_list:
            # Use the add method.
            self.add(glacier_list)

    def __repr__(self):
        return f"Glacier collection with {len(self._glaciers)} glaciers."

    def _repr_html_(self):
        # Pretty representation for notebooks.
        # Return the html representation of the summary dataframe.
        if len(self._glaciers) > 0:
            return self.summary()._repr_html_()
        else:
            pass

    def summary(self):
        """Returns a summary of the collection in the form of a pandas dataframe."""

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

            # Set the index name.
            df = df.reindex()
            df.index += 1
            df.index.name = "Glacier"
            return df

        else:
            pass

    def reset(self):
        """Reset all glaciers in the collection"""
        # If we have glaciers,
        if self._glaciers:
            # Reset all of them.
            for glacier in self.glaciers:
                glacier.reset()
        else:
            print("Collection does not contain any glaciers to reset.")

    def _check_collection(self):
        """Utility method. Check if the glaciers obey the collection rules.
        Make sure that the glaciers have the same bed.
        """

        # If there is only one glacier in the collection, it is always ok.
        if len(self._glaciers) <= 1:
            return True

        # Compare the glacier beds
        beds = [glacier.bed.bed_h for glacier in self._glaciers]
        # Do we get all ok?
        ok = []
        # We only have to check all the beds against one reference bed.
        for bed in beds[1:]:
            # Is the pair equal?
            ok.append(np.array_equal(beds[0], bed))

        # Any fails?
        ok = np.asarray(ok).all()
        return ok

    @property
    def glaciers(self):
        """Glaciers stored in the collection"""
        return self._glaciers

    @property
    def annual_mass_balance(self):
        """Glaciers mass balances"""
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
            See ``GlacierCollection.change_attributes`` for more.
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
        """Adds one or more glaciers to the collection. Glaciers have to have the same slope.

        Parameters
        ----------
        glacier : oggm.edu Glacier object or array_like with
        Glacier objects
        """
        # Check if iterable
        if isinstance(glacier, Sequence):
            for glacier in glacier:
                # Check that glacier is of the right type.
                if not isinstance(glacier, Glacier):
                    raise TypeError(
                        "Glacier collection can only contain glacier objects."
                    )
                # Is the glacier already in the collection?
                elif glacier in self._glaciers:
                    raise AttributeError("Glacier is already in collection")
                # If no throws, add it.
                self._glaciers.append(glacier)
        # If not iterable
        else:
            # Check that glacier is of the right type.
            if not isinstance(glacier, Glacier):
                raise TypeError("Glacier collection can only contain glacier objects.")
            # Is the glacier already in the collection?
            elif glacier in self._glaciers:
                raise AttributeError("Glacier is already in collection")
            # If no throws, add it.
            self._glaciers.append(glacier)

    def change_attributes(self, attributes_to_change):
        """Change the attribute(s) of the glaciers in the collection.

        Parameters
        ----------

        attributes_to_change : dict
            Dictionary where the key value pairs follow the structure:
            ``{"key": [n values], ...}``, where "key" matches an attribute
            of the glacier and n matches the length of the collection.
            Valid keys are:

            * ``gradient``
            * ``ela``
            * ``basal_sliding``
            * ``creep``
            * ``normal_years``
            * ``surging_years``
            * ``basal_sliding_surge``

            Values should be either numeric or a partial
            mathematical expression (string) e.g. ``"* 10"``: this would evaluate
            to multiplying the current value by a factor 10. Pass an empty
            string to leave the attribute unaffected.
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
            elif not isinstance(values, Sequence):
                raise TypeError("Provided value should be in the form of a list/tuple")
            elif not len(values) == len(self.glaciers):
                raise ValueError(
                    "Numbers of values provided does not match size of collection."
                )
            # If all passes
            else:
                # Set values and glaciers.
                for (glacier, value) in zip(self.glaciers, values):
                    # Should we act on the glacier or mass balance?
                    if key in mb_attrs:
                        obj = glacier.mass_balance
                    # Just the glacier
                    else:
                        obj = glacier

                    # If value is a string (a partial expression) we set the value
                    # using the expression_parser.
                    if isinstance(value, str):
                        # Get the current value of the attribute.
                        curr_value = getattr(obj, key)
                        # Calculate the value based on the partial expression.
                        value = expression_parser(value, curr_value)
                    # If value is not a string we can just assign it directly.
                    # Use built in setattr. Should respect the defined
                    # setters, with error messages an such.
                    setattr(obj, key, value)

    def _partial_progression(self, year, glacier):
        """Function used to create partial tasks which can be passed to pool of workers.

        Parameters
        ----------
        year : int
            Which year to progress the glacier
        glacier : oggm_edu.Glacier
            Instance which should be progressed.
        """
        # Simply progress the glacier to desired year.
        glacier.progress_to_year(year)
        # Return the glacier.
        return glacier

    def progress_to_year(self, year):
        """Progress the glaciers within the collection to
        the specified year.

        Parameters
        ----------
        year : int
            Which year to progress the glaciers.
        """
        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")

        # Create a partial function, with the year specified.
        partial_progression = partial(self._partial_progression, year)

        # Pool context manager.
        with Pool() as p:
            # We use pool.map to evaluate the partial function on all glaciers in the collection.
            # After this, "update" the collection with the resulting glaciers.
            self._glaciers = p.map(partial_progression, self._glaciers)

    def _partial_eq_progression(self, years, t_rate, glacier):
        """Function used to create partial tasks which can be passed to pool of workers.
        Progress to equilibrium state.

        Parameters
        ----------
        years : int
            Specify the number of years during which we try to find
            an equilibrium state.
        t_rate : float
            Specify how slow the glacier is allowed to change without
            reaching equilibrium.
        glacier : oggm_edu.Glacier
            Instance which should be progressed.
        """
        # Simply progress the glacier to desired year.
        glacier.progress_to_equilibrium(years=years, t_rate=t_rate)
        # Return the new glacier
        return glacier

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

        partial_eq_progression = partial(self._partial_eq_progression, years, t_rate)

        # Pool context manager.
        with Pool() as p:
            # We use pool.map to evaluate the partial function on all glaciers in the collection.
            # After this, "update" the collection with the resulting glaciers.
            self._glaciers = p.map(partial_eq_progression, self._glaciers)

    @edu_plotter
    def plot(self):
        """Plot the glaciers in the collection to compare them."""

        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")

        elif not self._check_collection():
            msg = ("We can only plot glacier surfaces if the glaciers "
                   "all have the same bed. Try .plot_side_by_side() "
                   "instead.")
            raise ValueError(msg)

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
                    label=f"Glacier {i+1} at year" + f" {glacier.age}",
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
                elas_d[key] += f"{i+1}, "

            # Loop the unique ELAs.
            for ela, string in elas_d.items():
                # Add the annotation.
                ax.text(
                    glacier.bed.distance_along_glacier[-1],
                    ela + 10,
                    f"ELA glacier {string[:-2]}",
                    ha="right",
                    va="bottom",
                )
                # Plot the ELA
                ax.axhline(ela, ls="--", zorder=1)

        # axis labels.
        ax.set_xlabel("Distance along glacer [km]")
        ax.set_ylabel("Altitude [m]")
        # Add 2% of bed length as padding to the plot.
        ax.set_xlim((0, gl1.bed.distance_along_glacier[-1] * 1.02))
        ax.set_facecolor("#ADD8E6")
        plt.legend(loc="lower left")
        # Add a second legend with infos.
        # It would be cool to only show attributes that are different.
        labels = []
        for glacier in self._glaciers:
            # Create the label
            label = (
                f"Type: {type(glacier).__name__}\n"
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
    def plot_side_by_side(self):
        """Plot the collection but side by side.

        Useful for glaciers with different beds
        """
        if len(self._glaciers) < 1:
            raise ValueError("Collection is empty")

        # Get the axes
        fig, axes = plt.subplots(
            nrows=2, ncols=len(self._glaciers),
            gridspec_kw={"height_ratios": [2, 1]},
            sharex=True,
        )

        # Loop over the collection.
        if len(self._glaciers) == 1:
            self._glaciers[0].plot(axes=axes)
        else:
            ax0 = None
            for i, (axs, glacier) in enumerate(zip(axes.T, self._glaciers)):
                glacier.plot(axes=axs, title_number=i+1)
                if ax0 is None:
                    xr = glacier._decide_xlim()
                    yr = glacier._decide_ylim()
                    ax0 = axs[0]
                    ax1 = axs[1]
                else:
                    xr = np.append(xr, glacier._decide_xlim())
                    yr = np.append(yr, glacier._decide_ylim())
                    axs[0].sharey(ax0)
                    axs[1].sharey(ax1)
            ax0.set_xlim(np.min(xr), np.max(xr))
            ax0.set_ylim(np.min(yr), np.max(yr))
        plt.tight_layout()

    @edu_plotter
    def plot_history(self):
        """Plot the histories of the collection."""

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
                    label=(
                        f"Glacier {i+1}\n"
                        f"Type: {type(glacier).__name__}\n"
                        f"ELA: {glacier.ela}\n"
                        f"MB grad: {glacier.mb_gradient}\n"
                        f"Age: {glacier.age}\n"
                        f"Creep: {glacier.creep:.2e}\n"
                        f"Sliding: {glacier.basal_sliding}"
                    ),
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
        """Plot the mass balance(s) for the glaciers in the collection."""

        fig, ax = plt.subplots()

        # How many unique ELAS do we have?
        elas = []

        # Plot annual mass balance for each glacier.
        for i, glacier in enumerate(self.glaciers):
            ax.plot(
                glacier.annual_mass_balance,
                glacier.bed.bed_h,
                label=f"Glacier {i+1}, " + f"gradient {glacier.mass_balance.gradient}",
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
                elas_d[key] += f"{i+1}, "

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
