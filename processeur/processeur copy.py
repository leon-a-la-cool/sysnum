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


    incrvalue = Mux(Defer(1, lambda : jump),Constant("0"*6 + "1"),Defer(7, lambda: jvalue))
    incroffset = adder(offset, incrvalue,Constant("0"),None)[0]
    instr = ROM(7, 32, offset)
    
    #interpretation

    opcode = instr[25:]
    rd = instr[20:25]
    valopcode = kdemux(opcode,Constant("1"),7)
    funct3 = instr[17:20]
    rs1=instr[12:17]
    rs2=instr[7:12]
    funct7=instr[0:7]
    immItype = funct7 + rs2
    immJtype =  immItype + rs1 + funct3

    #jump

    jal = valopcode[111]
    
    jvalue = immJtype[13:]
    jump = jal

    #binop entre deux regs
    add = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0000000"))
    sub = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0100000"))
    or_ = valopcode[51] & eq(funct3,Constant("110")) & eq(funct7,Constant("0000000"))
    and_ = valopcode[51] & eq(funct3,Constant("111")) & eq(funct7,Constant("0000000"))
    xor = valopcode[51] & eq(funct3,Constant("100")) & eq(funct7,Constant("0000000"))
    slt = valopcode[51] & eq(funct3,Constant("010")) & eq(funct7,Constant("0000000"))
    sltu = valopcode[51] & eq(funct3,Constant("011")) & eq(funct7,Constant("0000000"))
    op_entre_deux_reg = add | sub | or_ | and_ | xor |slt |sltu

    #binop entre regs et imm

    addi = valopcode[19] & eq(funct3,Constant("000"))
    xori = valopcode[19] & eq(funct3,Constant("100"))
    ori = valopcode[19] & eq(funct3,Constant("110"))
    andi = valopcode[19] & eq(funct3,Constant("111"))

    
    
    op_entre_reg_et_i = addi | xori | ori | andi

    ##

    waddr = rd 
    raddr1 = rs1 
    raddr2 = rs2 


    op = op_entre_deux_reg | op_entre_reg_et_i
    wenable = op

    rdata1,rdata2 = regblock(waddr,Defer(32,lambda:wdata),wenable,raddr1,raddr2)

    allowin1 = op
    

    inalu1 = Mux(allowin1,zero,rdata1)
    inalu2 = Mux(op_entre_reg_et_i,Mux(op_entre_deux_reg,zero,rdata2),Constant("0"*20)+immItype)
    
    vsub = (sub |slt |sltu) & op_entre_deux_reg 
    vnot = op_entre_deux_reg & Constant("0")
    vand = (op_entre_deux_reg & and_) | (op_entre_reg_et_i & andi)
    vor = (op_entre_deux_reg & or_) | (op_entre_reg_et_i & ori)
    vxor = (op_entre_deux_reg & xor) | (op_entre_reg_et_i & xori)

    (outalu,overflow,negative,null) = alu(inalu1,inalu2,vsub,vnot,vand,vor,vxor,32)

    wdata = Mux(slt|sltu,outalu,zero[:31] + negative) 
    return wdata

def main():
    x = Input(1)
    a = processeur()
    a.set_as_output("out")
    


    