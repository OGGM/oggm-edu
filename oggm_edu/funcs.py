"""oggm-edu package: useful functions diffult to place elsewhere"""
import urllib
from functools import wraps
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from oggm import cfg

graphics_url = (
    "https://raw.githubusercontent.com/OGGM/glacier-graphics/master/"
    "glacier_intro/png/glacier_{:02d}.png"
)

PARAMS = {'figsize': (9, 6)}


class mpl_figsize:
    """Homegrown context manager to avoid a bug

    https://github.com/matplotlib/matplotlib/issues/25041
    """
    def __init__(self, figsize):
        self.figsize = plt.rcParams['figure.figsize']
        plt.rcParams['figure.figsize'] = figsize
    def __enter__(self):
        return None
    def __exit__(self, type, value, traceback):
        plt.rcParams['figure.figsize'] = self.figsize


def plot_glacier_graphics(num="01", title=False, ax=None):
    """Add one of the OGGM-edu glacier graphics to the current jupyter cell.

    Source images: https://github.com/OGGM/glacier-graphics/tree/master/glacier_intro/png

    Explanation: https://edu.oggm.org/en/latest/glacier_basics.html

    Parameters
    ----------
    num : int or str
        number from 01 to 11
    title : str
        add a title to the plot
    ax : matplotlib axis
        the axis on which to plot the image (if None, a new figure is created)

    Returns
    -------
    the plot axis
    """
    if ax is None:
        _, ax = plt.subplots()
    ax.imshow(Image.open(urllib.request.urlopen(graphics_url.format(int(num)))))
    ax.patch.set_visible(False)
    ax.axis("off")
    if title:
        plt.title(title)
    return ax


def initalize_oggm(logging_level="CRITICAL"):
    """Initialize OGGM parameters.

    Parameters
    ----------
    logging_level : str
       https://docs.oggm.org/en/stable/generated/oggm.cfg.set_logging_config.html

    Returns
    -------
    none
    """
    cfg.initialize_minimal(logging_level=logging_level)


def set_params(figsize=(9, 6)):
    PARAMS['figsize'] = figsize


def edu_plotter(func):
    """Decorator to apply to all plotting functions in OGGM-Edu.

    Parameters
    ----------
    func : function
        the function or method to decorate

    Returns
    -------
    the decorated function
    """

    @wraps(func)
    def context_wrapper(
        *args,
        figsize=None,
        sns_context="notebook",
        sns_axes_style="ticks",
        **kwargs,
    ):
        if not figsize:
            figsize = PARAMS['figsize']

        with mpl_figsize(figsize), \
                sns.plotting_context(sns_context), \
                sns.axes_style(sns_axes_style):
            return func(*args, **kwargs)
    return context_wrapper


def expression_parser(expression, numeric):
    """Parse an uncomplete math expression e.g. '* 10' and apply it to supplied attribute.

    Parameters
    ----------
    expression : string
        Incomplete math expression in the form '* 5' or '- 10'. Can also be empty to leave
        numeric un-affected.
    numeric : int or float
        Value to evaluate against expression.
    Returns
    -------
    The full expression evaluated.
    """

    # is expression a string?
    if not isinstance(expression, str):
        raise TypeError("expression should be a string.")

    elif not isinstance(numeric, (int, float)):
        raise TypeError("numeric should be an integer or a float.")
    # If expression is empty, we return the numeric.
    elif expression == "":
        return numeric

    else:
        # Extract the operator
        operator = expression[0]
        if operator not in ["*", "/", "+", "-"]:
            raise ValueError(
                "First part of expression should be either one of *, /, +, -."
            )
        # Extract the factor
        factor = float(expression[1:])
        # Create a table of possible expressions. Then we just pick the correct one for return.
        expression_dict = {
            "*": numeric * factor,
            "/": numeric / factor,
            "+": numeric + factor,
            "-": numeric - factor,
        }

        return expression_dict[operator]


def cp_glen_a(t):
    """This implements the conversion between temperature and Glen's A,
       as eq. 3.35 in  The physics of glaciers by Cuffey and Paterson.

    Parameters
    ----------
    t : int, float
        Temperature in degrees Celsius. Should be below 0.
    """

    # Constants.
    a_star = 3.5 * 1e-25
    q_plus = 115_000
    t_star = 263 + 7 * 1e-8
    q_minus = 60_000
    r = 8.314

    # Check if temp is below 0.
    if t > 0:
        raise ValueError("Supplied temperature should be below 0.")

    # Convert to Kelvin
    t = t + 273
    t_h = t + 7 * 1e-8

    if t < t_star:
        q_c = q_minus
    else:
        q_c = q_plus

    return a_star * np.exp(-(q_c / r) * (1 / t_h - 1 / t_star))
