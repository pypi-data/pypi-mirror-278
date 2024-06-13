from ..scripts import Humon, Scripted
#=============================================================================

def Dbytes(sizes, second=Scripted.DATA01):
    if not sizes or sizes == Scripted.DATA02 or sizes < 0:
        return Scripted.DATA09 + second
    nomos = 0
    POWEO = 1024
    POWER = Humon.DATA01
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    moonus = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + second
    return moonus

#=============================================================================

def Hbytes(sizes, second=Scripted.DATA01):
    if not sizes or sizes == Scripted.DATA02 or sizes < 0:
        return Scripted.DATA08 + second
    nomos = 0
    POWEO = 1024
    POWER = Humon.DATA02
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    moonus = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + second
    return moonus

#=============================================================================

def Gbytes(sizes, second=Scripted.DATA01):
    if not sizes or sizes == Scripted.DATA02 or sizes < 0:
        return Scripted.DATA01 + second
    nomos = 0
    POWEO = 1024
    POWER = Humon.DATA01
    while sizes > POWEO:
        sizes /= POWEO
        nomos += 1
    moonus = str(round(sizes, 2)) + Scripted.DATA02 + POWER[nomos] + second
    return moonus

#=============================================================================
