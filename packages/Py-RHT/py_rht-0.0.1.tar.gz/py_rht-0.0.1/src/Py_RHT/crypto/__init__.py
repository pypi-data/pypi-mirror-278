"""
A submodule for Py_RHT containing cryptography functions

supported cryptos
-----------------
Xor : encode/decode (var_xor)\n 
Base 64 : encode(b64_encode)  / decode(b64_decode)\n

"""

#all module import
__all__ = ["xor","b64", "bitshift", 'reverse' , 'decimal']

#specific imports

#   XOR imports
from .xor import xor
from .xor import bruteforce

#   base 64 imports
from .b64 import b64_decode
from .b64 import b64_encode

from .reverse import reverse
from .bitshift import bitshift
from .decimal import toDecimal
from .decimal import fromDecimal

