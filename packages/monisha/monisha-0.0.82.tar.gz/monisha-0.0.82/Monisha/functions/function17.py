import os
import random
from ..scripts import Scripted
from urllib.parse import unquote
from urllib.parse import urlparse
from .collections import SMessage
#=========================================================================

class Filename:

    async def get01(extension=None):
        mainos = str(random.randint(10000, 100000000000000))
        moonus = mainos + extension if extension else mainos
        return moonus

#=========================================================================

    async def get02(filename):
        nameas = str(filename)
        finame = os.path.splitext(nameas)[0]
        exexon = os.path.splitext(nameas)[1]
        exoexo = exexon if exexon else Scripted.DATA06
        moonus = finame if finame else Scripted.DATA13
        return SMessage(filename=moonus, extension=exoexo)

#=========================================================================

    async def get03(filelink):
        try:
            findne = urlparse(filelink)
            fnameo = os.path.basename(findne.path)
            moonus = unquote(fnameo)
            return SMessage(filename=moonus, errors=None)
        except Exception as errors:
            return SMessage(filename=Scripted.DATA14, errors=errors)

#=========================================================================

    async def get04(location):
        try:
            moonus = str(os.path.basename(location))
            return SMessage(filename=moonus, errors=None)
        except Exception as errors:
            return SMessage(filename=Scripted.DATA14, errors=errors)

#=========================================================================
