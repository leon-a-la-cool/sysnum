from lib_carotte import *
from processeur.registre import regblock
from processeur.nadder import adder
from processeur.kdemux import kdemux
from processeur.eq import eq
from processeur.alu import alu

def processeur():

    zero = Constant("0"*32)

    #lecture de l'instruction

    offset = Reg(Defer(7, lambda : incroffset))
    incroffset = adder(offset, Constant("0"*6 + "1"),Constant("0"),None)[0]
    instr = ROM(7, 32, offset)
    
    #interpretation

    opcode = instr[25:]
    rd = instr[20:25]
    valopcode = kdemux(opcode,Constant("1"),7)
    funct3 = instr[17:20]
    rs1=instr[12:17]
    rs2=instr[7:12]
    funct7=instr[0:7]

    #add et sub
    add = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0000000"))
    sub = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0100000"))

    op_entre_deux_reg = add | sub

    #addi

    addi = valopcode[19] & eq(funct3,Constant("000"))
    immItype = funct7 + rs2


    op_entre_reg_et_i = addi

    ##

    waddr = rd 
    raddr1 = rs1 
    raddr2 = rs2 



    wenable = op_entre_deux_reg | op_entre_reg_et_i


    rdata1,rdata2 = regblock(waddr,Defer(32,lambda:wdata),wenable,raddr1,raddr2)

    allowin1 = op_entre_deux_reg | op_entre_reg_et_i
   

    inalu1 = Mux(allowin1,zero,rdata1)
    inalu2 = Mux(op_entre_reg_et_i,Mux(op_entre_deux_reg,zero,rdata2),Constant("0"*20)+immItype)
    
    vsub = sub & op_entre_deux_reg
    vnot = op_entre_deux_reg & Constant("0")
    vand = op_entre_deux_reg & Constant("0")
    vor = op_entre_deux_reg & Constant("0")
    vxor = op_entre_deux_reg & Constant("0")

    (wdata,overflow,negative,null) = alu(inalu1,inalu2,vsub,vnot,vand,vor,vxor,32)

    return wdata

def main():
    x = Input(1)
    a = processeur()
    a.set_as_output("out")
    


    