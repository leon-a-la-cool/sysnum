from lib_carotte import *
from processeur.kmux import *
from processeur.kdemux import *


allow_ribbon_logic_operations(True)


def reg(wdata: Variable,wenable: Variable):
    
    
    rdata=Reg(Defer(wdata.bus_size,lambda : y))
    y = Mux(wenable,rdata,wdata)
    return rdata



def regblock(waddr,wdata,wenable,raddr1,raddr2,n,k): #k puissance de 2 du nombre de registres, n taille des données

    

    wdatalist = kdemux(waddr,wdata,k)
    wenablelist = kdemux(waddr,wenable,k)

    lrdata = [Constant("0"*n)]
    for i in range(1,2**k):
        lrdata.append(reg(wdatalist[i],wenablelist[i]))
    rdata1 = kmux(raddr1,lrdata,k)
    rdata2 = kmux(raddr2,lrdata,k)
    return rdata1,rdata2



def main() -> None:
    nbbits = 8
    waddr = Input(5)
    wdata = Input(nbbits)
    wenable = Input(1)
    raddr1 = Input(5)
    raddr2 = Input(5)
    rdata1,rdata2 = regblock(waddr,wdata,wenable,raddr1,raddr2,5)
    rdata1.set_as_output("radata1")
    rdata2.set_as_output("radata2")
    