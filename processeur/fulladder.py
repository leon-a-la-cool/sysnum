
from lib_carotte import *
allow_ribbon_logic_operations(True)


def half_adder(a: Variable, b: Variable) -> typing.Tuple[Variable, Variable]:
    s = a^b
    c = a&b
    return (s,c)


def full_adder(a: Variable, b: Variable, c: Variable) -> typing.Tuple[Variable, Variable]:
    s,r = half_adder(a,b)
    s2,c2 = half_adder(s,c)
    r2 = r | c2 
    return (s2,r2)

def main() -> None:
   a = Input(1)
   b = Input(1)
   c = Input(1)
   (result, out_carry) = full_adder(a, b, c)
   result.set_as_output("result")
   out_carry.set_as_output("out_c")


