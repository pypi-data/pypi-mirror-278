import os
import time
from ..scripts import Folder
from ..scripts import Scripted
#================================================================================

class Location:

    async def mak01(dname=Folder.DATA07):
        direos = str(dname)
        osemse = os.getcwd()
        moonse = os.path.join(osemse, direos, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================

    async def mak02(dname=Folder.DATA07):
        direos = str(dname)
        osemse = os.getcwd()
        timeso = str(round(time.time()))
        moonse = os.path.join(osemse, direos, timeso, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================

    async def mak03(uid, dname=Folder.DATA07):
        usered = str(uid)
        direos = str(dname)
        osemse = os.getcwd()
        timeso = str(round(time.time()))
        moonse = os.path.join(osemse, direos, usered, timeso, Scripted.DATA01)
        moonse if os.path.exists(moonse) else os.makedirs(moonse)
        return moonse

#================================================================================
