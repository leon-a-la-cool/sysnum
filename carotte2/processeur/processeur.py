from lib_carotte import *
from processeur.registre import regblock
from processeur.nadder import adder
from processeur.eq import eq
from processeur.alu import alu
from processeur.septseg import convert
import math


def processeur():
    nbbit = 16

    zero = Constant("0"*nbbit)



    #lecture de l'instruction

    offset = Reg(Defer(7, lambda : incroffset))


    incrvalue = Mux(Defer(1,lambda : branch_or_jump ),Constant("0"*6 + "1"),Defer(7, lambda: jvalue))
    incroffset = adder(offset, incrvalue,Constant("0"),None)[0]
    instr = ROM(7, 32, offset)
    


    #interpretation

    opcode = instr[25:]
    rd = instr[20:25]
    #valopcode = kdemux(opcode,Constant("1"),7)
    funct3 = instr[17:20]
    rs1=instr[12:17]
    rs2=instr[7:12]
    funct7=instr[0:7]
    immItype = funct7 + rs2
    non_rot_immJtype =  (immItype + rs1 + funct3)
    immJtype = non_rot_immJtype[0]+ non_rot_immJtype[12:] + non_rot_immJtype[11] + non_rot_immJtype[1:11]
    immBtype = instr[0]+rd[4]+funct7[1:]+rd[:4]
    immStype = funct7 + rd
    immUtype = instr[:20]

    #lui

    i55=Constant("0110111")
    i111=Constant("1101111")
    i99=Constant("1100011")
    i51=Constant("0110011")
    i19=Constant("0010011")
    i3=Constant("0000011")
    i35=Constant("0100011")

    lui = eq(opcode,i55)



    #jump


    jal = eq(opcode,i111)
    opcode99 = eq(opcode,i99)
    beq = opcode99 & eq(funct3,Constant("000"))
    bneq = opcode99 & eq(funct3,Constant("001"))
    blt = opcode99 & eq(funct3,Constant("100"))
    bge = opcode99 & eq(funct3,Constant("101"))

    branching = (beq & Defer(1,lambda : null)) | (bneq & Not(Defer(1,lambda : null))) | (blt & Defer(1,lambda : negative)) | (bge & Not(Defer(1,lambda : negative)))

    
    jump = jal 
    
    branch_or_jump = branching|jump

    #jvalue = adder(Mux(jump,immBtype[5:],immJtype[13:]),Constant("0000010"),Constant("0"),None)[0]
    jvalue = Mux(jump,immBtype[4:],immJtype[12:])[:7]

    #binop entre deux regs
    opcode51 = eq(opcode,i51)
    add = opcode51 & eq(funct3,Constant("000")) & eq(funct7,Constant("0000000"))
    sub = opcode51 & eq(funct3,Constant("000")) & eq(funct7,Constant("0100000")) | beq | bneq | blt | bge
    orbinop= opcode51 & eq(funct3,Constant("110")) & eq(funct7,Constant("0000000"))
    andbinop = opcode51 & eq(funct3,Constant("111")) & eq(funct7,Constant("0000000"))
    xor = opcode51 & eq(funct3,Constant("100")) & eq(funct7,Constant("0000000"))
    slt = opcode51 & eq(funct3,Constant("010")) & eq(funct7,Constant("0000000"))
    sltu = opcode51 & eq(funct3,Constant("011")) & eq(funct7,Constant("0000000"))
    op_entre_deux_reg = add | sub | orbinop| andbinop | xor |slt |sltu

    #binop entre regs et imm
    opcode19=eq(i19,opcode)
    addi = opcode19 & eq(funct3,Constant("000"))
    xori = opcode19 & eq(funct3,Constant("100"))
    ori = opcode19 & eq(funct3,Constant("110"))
    andi = opcode19 & eq(funct3,Constant("111"))

    
    
    op_entre_reg_et_i = addi | xori | ori | andi

    ##mémoire


    lw = eq(opcode,i3) & eq(funct3,Constant("010"))
    sw = eq(opcode,i35) & eq(funct3,Constant("010"))

    load = lw
    store = sw

    #7 seg
    call = eq(opcode,Constant("1110011"))
    


    ##

    waddr = Mux(call,rd[1:],Constant("1000"))
    raddr1 = Mux(call,rs1[1:],Constant("1000"))
    raddr2 = rs2[1:]


    op = op_entre_deux_reg | op_entre_reg_et_i | load | store
    wenable = (op_entre_deux_reg & Not(opcode99))| load | lui |op_entre_reg_et_i |call

    rdata1,rdata2 = regblock(waddr,Defer(nbbit,lambda:wdata),wenable,raddr1,raddr2,nbbit,4)

    allowin1 = op
    

    inalu1 = Mux(allowin1,zero,rdata1)
    inalu2 = Mux(store,Mux(load,Mux(op_entre_reg_et_i,Mux(op_entre_deux_reg,zero,rdata2),Constant("0"*(nbbit-12))+immItype),Constant("0"*(nbbit-12))+ immItype),Constant("0"*(nbbit-12))+immStype)
    
    vsub = (sub |slt |sltu|beq |bge |blt |bneq) & op_entre_deux_reg 
    vnot = op_entre_deux_reg & Constant("0")
    vand = (op_entre_deux_reg & andbinop) | (op_entre_reg_et_i & andi)
    vor = (op_entre_deux_reg & orbinop) | (op_entre_reg_et_i & ori)
    vxor = (op_entre_deux_reg & xor) | (op_entre_reg_et_i & xori)

    (outalu,overflow,negative,null) = alu(inalu1,inalu2,vsub,vnot,vand,vor,vxor,nbbit)

    ramWenable = store
    ramRaddr = Mux(load,zero,outalu)[(nbbit-8):]
    ramWaddr = Mux(store,zero,outalu)[(nbbit-8):]
    ramWdata = rdata2

    ramdata = RAM(8,nbbit,ramRaddr,ramWenable,ramWaddr,ramWdata)
    

    if nbbit >=20:
        u = Constant("0"*(nbbit-20)) + immUtype
    else:
        u = immUtype[20-nbbit:]
    
    wdata = Mux(call,Mux(lui,Mux(load,Mux(jump,Mux(slt|sltu,outalu,zero[:nbbit-1] + negative),Constant("0"*(nbbit-7)) + incroffset),ramdata),u),Constant("0"*(nbbit-14)) + convert(rdata1[nbbit-7:]))



    return rdata1,raddr1,wenable,wdata,waddr

def main():
   # x = Input(0)
    a = processeur()
   # a[0].set_as_output("out")
   # a[1].set_as_output("raddresse")
   # a[2].set_as_output("we")
   # a[3].set_as_output("rwdata")
   # a[4].set_as_output("rwaddr")