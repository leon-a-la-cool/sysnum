from lib_carotte import *
allow_ribbon_logic_operations(True)


def kmux(c : Variable,l,k : int)->Variable: #prend en argument une liste de variables
    if k==1:
        return Mux(c[0],l[0],l[1])
    else:
        return Mux(c[0],kmux(c[1:],l[:(2**(k-1))],k-1),kmux(c[1:],l[(2**(k-1)):],k-1))


def main():
    k=4
    nbbits = 16
    addr = Input(k)

    l=[]
    for i in range(2**k):
        l.append(Input(nbbits))

    o = kmux(addr,l,k)
    o.set_as_output("out")