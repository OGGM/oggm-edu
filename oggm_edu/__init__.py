__version__ = "0.1.0b"

from oggm_edu.funcs import plot_glacier_graphics, initalize_oggm, set_params
from oggm_edu.glacier import Glacier, SurgingGlacier
from oggm_edu.glacier_bed import GlacierBed
from oggm_edu.glacier_collection import GlacierCollection
from oggm_edu.mass_balance import MassBalance

# Initialize on import
initalize_oggm()
