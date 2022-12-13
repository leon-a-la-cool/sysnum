from lib_carotte import *

allow_ribbon_logic_operations(True)

def eq(a,b):
    n = a.bus_size
    c = Not(Xor(a,b))
    l=[c[0]]
    for i in range(n):
        l.append(And(l[-1],c[i]))
    return l[-1]


def main():
    a=Input(4)
    b=Input(4)
    c = eq(a,b)
    c.set_as_output("o")