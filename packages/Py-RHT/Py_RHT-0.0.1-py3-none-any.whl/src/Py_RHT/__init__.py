"""
A module built to help developers with little offhand tasks
"""
__all__ =  ["crypto","bin","forensics","programming"]

#submodule imports
from . import crypto
from . import forensics
from . import programming


#base module imports
from .bin import bin