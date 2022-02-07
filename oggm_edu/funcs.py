"""oggm-edu package: useful functions diffult to place elsewhere"""
import urllib
from functools import wraps
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from oggm import cfg

graphics_url = (
    "https://raw.githubusercontent.com/OGGM/glacier-graphics/master/"
    + "glacier_intro/png/glacier_{:02d}.png"
)


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
        *args, sns_context="notebook", sns_axes_style="ticks", figsize=(12, 9), **kwargs
    ):
        with \
            mpl.rc_context({"figure.figsize": figsize}), \
            sns.plotting_context(sns_context), \
            sns.axes_style(sns_axes_style)\
                :
            return func(*args, **kwargs)

    return context_wrapper
