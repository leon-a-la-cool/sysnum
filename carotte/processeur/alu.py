from lib_carotte import *
from processeur.nadder import adder 


allow_ribbon_logic_operations(True)

def alu(a: Variable,b: Variable,vsub: Variable,vnot: Variable,vand: Variable,vor: Variable,vxor: Variable,n: int) ->  typing.Tuple[Variable, Variable]:
    b2 = Mux(vsub,b,Constant("1"*n)^b)
    s,v = adder(a,b2,vsub)
    s2 = Mux(vnot,s,Not(a)) #not
    s3 = Mux(vand, s2, a & b)
    s4 = Mux (vor, s3, a | b )
    s5 = Mux(vxor, s4, Xor(a,b))
    neg = s5[0]
    z = Constant("0")
    for i in range(n):
        z = z | s5[i]
    return (s5,v,neg,Not(z))






def main() -> None:
    n=4 #nombre de bits
    a = Input(n)
    b = Input(n)
    vsub = Input(1)
    vnot = Input(1)
    vand = Input(1)
    vor = Input(1)
    vxor=Input(1)
    (result, overflow,negative,null) = alu(a,b,vsub,vnot,vand,vor,vxor,n)
    result.set_as_output("result")
    overflow.set_as_output("overflow")
    negative.set_as_output("negative")
    null.set_as_output("null")

