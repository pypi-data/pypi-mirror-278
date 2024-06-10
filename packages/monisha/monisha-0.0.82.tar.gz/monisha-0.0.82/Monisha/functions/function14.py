import os
from pathlib import Path
from .function04 import Eimes
from .collections import SMessage
#======================================================================

class Locations:

    async def get01(directory, stored=None):
        sos = stored if stored else []
        for item in Path(directory).rglob('*'):
            if item.is_dir():
                continue
            else:
                sos.append(str(item))

        sos.sort()
        return SMessage(allfiles=sos, numfiles=len(sos))

#======================================================================

    async def get02(directory, stored=None, skip=Eimes.DATA00):
        sos = stored if stored else []
        for patho in directory:
            if patho.upper().endswith(skip):
                continue
            else:
                sos.append(patho)

        sos.sort()
        return SMessage(allfiles=sos, numfiles=len(sos))

#======================================================================
