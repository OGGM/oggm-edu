__version__ = "0.1.0b"

from oggm_edu.funcs import plot_glacier_graphics, initalize_oggm
from oggm_edu.glacier import Glacier, SurgingGlacier
from oggm_edu.glacierBed import GlacierBed
from oggm_edu.glacierCollection import GlacierCollection
from oggm_edu.massBalance import MassBalance

# Initialize on import
initalize_oggm()
