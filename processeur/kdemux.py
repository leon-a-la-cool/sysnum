from lib_carotte import *
allow_ribbon_logic_operations(True)





#2**k outputs

def kdemux(c : Variable,a :Variable,k : int): # renvoie une liste de variable
    n = a.bus_size
    if k==1:
        return Mux(c[0],a,Constant("0"*n)),Mux(c[0],Constant("0"*n),a)

    
    return kdemux(c[1:],Mux(c[0],a,Constant("0"*n)),k-1) + kdemux(c[1:],Mux(c[0],Constant("0"*n),a),k-1)



#def ndemux(c,a,n):
#    k = 0
#    while 2**k<n:
#        k+=1
#    p = n - 2**k
#    
#    kdemux(Constant("0"*(k-c.bus_size))+c,)

def main():
    k=4
    nbbits = 16
    addr = Input(k)
    i = Input(nbbits)
    r = kdemux(addr,i,k)
    for i in range(len(r)):
        (r[i]).set_as_output("out"+str(i))
