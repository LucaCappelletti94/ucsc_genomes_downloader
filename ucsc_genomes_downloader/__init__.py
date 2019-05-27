import warnings
warnings.simplefilter("ignore", category=DeprecationWarning)

from .download_genome import download_genome

__all__ = ["download_genome"]