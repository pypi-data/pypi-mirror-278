"""module for some regex wrappers for common parsing procedures"""

import sys

if sys.version_info >= (3, 12):
    from parsable.main import Parsable
    from parsable.collection import ParsableCollection
else:
    from parsable.main import Parsable
    from parsable.backports import ParsableCollection

__all__ = ["Parsable", "ParsableCollection"]
