
from lib_carotte import *
from processeur.fulladder import full_adder

def adder(a: Variable, b: Variable, c_in: Variable, i: int = None) -> typing.Tuple[Variable, Variable]:
    if i is None:
        i = a.bus_size-1
    if i == 0:
        return full_adder(a[i], b[i], c_in)
    (res_i, c_rest) = full_adder(a[i], b[i], c_in)
    (res_rest, c_out) = adder(a, b, c_rest, i-1)
    return (res_rest + res_i, c_out)

def main() -> None:
    n = 64
    a = Input(n)
    b = Input(n)
    c = Input(1)
    (result, out_carry) = adder(a, b, c)
    result.set_as_output("result")
    out_carry.set_as_output("out_carry")


