import quickstats

quickstats.core.methods._require_module("XRootD")

from .core import *
from .filesystem import *
from .xrd_helper import XRDHelper