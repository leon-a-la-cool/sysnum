from lib_carotte import*
from processeur.alu import alu
from processeur.kmux import kmux
from processeur.nadder import adder

allow_ribbon_logic_operations(True)

def add3(a):
    c=Constant("0101")
    ge = a[0] | (a[1] & (a[2] | a[3]))
    t=Constant("0011")
    ad=adder(a,t,Constant("0"))[0]
    resul=Mux(ge,a,ad)
    return(resul)

def septseg(a): #correspondant a un tour a droite en partant du haut puis celui du milieu 

    zero = Constant("0000000")
    l=[Constant("1111110"),Constant("0110000"),Constant("1101101"),Constant("1111001"),Constant("0110011"),Constant("1011011"),Constant("1011111"),Constant("1110000"),Constant("1111111"),Constant("1110011"),zero,zero,zero,zero,zero,zero]
    seg=kmux(a,l,4)
    return(seg)

def convert(nb):
    n1=Slice(0,2,nb)
    g=Constant("00")+n1
    r1=add3(g)
    g=Slice(1,4,r1)+nb[2]
    r2=add3(g)
    g=Slice(1,4,r2)+nb[3]
    r3=add3(g)
    g=Slice(1,4,r3)+nb[4]
    r4=add3(g)
    g=Slice(1,4,r4)+nb[5]
    r5=add3(g)
    g=Constant("0")+(r1[0]+(r2[0]+r3[0]))
    r6=add3(g)
    g=Slice(1,4,r6)+r4[0]
    r7=add3(g)
    g=r7+(r5+nb[6])
    units=Slice(5,9,g)
    tens=Slice(1,5,g)
    u=septseg(units)
    t=septseg(tens)
    return t+u


def main():
    nb=Input(7)
    rommm = ROM(7,32,Constant("0000000"))
    rammm = RAM(8,8,Constant("00000000"),Constant("0"),Constant("00000000"),Constant("00000000"))
    out = convert(nb)
    out.set_as_output("out")


