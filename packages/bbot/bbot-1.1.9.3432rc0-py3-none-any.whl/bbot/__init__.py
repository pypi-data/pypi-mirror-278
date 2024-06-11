# version placeholder (replaced by poetry-dynamic-versioning)
__version__ = "v1.1.9.3432rc"

# global app config
from .core import configurator

config = configurator.config

# helpers
from .core import helpers
