from lib_carotte import *
from processeur.nadder import adder 


allow_ribbon_logic_operations(True)

def alu(a: Variable,b: Variable,vsub: Variable,vnot: Variable,vand: Variable,vor: Variable,n: int) ->  typing.Tuple[Variable, Variable]:
    b2 = a^b
    s,v = adder(a,b2,vsub)
    s2 = Mux(vnot,s,Not(a)) #not
    s3 = Mux(vand, s2, a & b)
    s4 = Mux (vor, s3, a | b )
    neg = s4[n-1]
    z = Constant("0")
    for i in range(n-1):
        z = z | s4[i]
    return (s4,v,neg,Not(z))






def main() -> None:
    n=32 #nombre de bits
    a = Input(n)
    b = Input(n)
    vsub = Input(1)
    vnot = Input(1)
    vand = Input(1)
    vor = Input(1)
    (result, overflow,negative,null) = alu(a,b,vsub,vnot,vand,vor,n)
    result.set_as_output("result")
    overflow.set_as_output("overflow")
    negative.set_as_output("negative")
    null.set_as_output("null")

