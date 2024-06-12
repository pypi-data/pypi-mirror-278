from .init import *

# import everything in `__main__` instead here because
# caller doesn't need import ALL lib modules of this package,
# otherwise `from felixlib.general import *` will import `felixlib.__init__` (this file) first
# would import ALL modules
