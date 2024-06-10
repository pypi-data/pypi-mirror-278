import random
from ..scripts import Strine, Scripted
#=======================================================================================

async def Randoms(length=32, message=Strine.DATA04):
    raumes = random.randint(10, length)
    ouoing = Scripted.DATA01.join(random.choice(message) for _ in range(raumes))
    return ouoing

#=======================================================================================
