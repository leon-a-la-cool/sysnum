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


    incrvalue = Mux(Defer(1,lambda : branch_or_jump ),Constant("0"*6 + "1"),Defer(7, lambda: jvalue))
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
    non_rot_immJtype =  (immItype + rs1 + funct3)
    immJtype = non_rot_immJtype[0]+ non_rot_immJtype[12:] + non_rot_immJtype[11] + non_rot_immJtype[1:11]
    immBtype = instr[0]+rd[4]+funct7[1:]+rd[:4]
    immStype = funct7 + rd


    #lui

    lui = valopcode[55]



    #jump

    jal = valopcode[111]
    beq = valopcode[99] & eq(funct3,Constant("000"))
    bneq = valopcode[99] & eq(funct3,Constant("001"))
    blt = valopcode[99] & eq(funct3,Constant("100"))
    bge = valopcode[99] & eq(funct3,Constant("101"))

    branching = (beq & Defer(1,lambda : null)) | (bneq & Not(Defer(1,lambda : null))) | (blt & Defer(1,lambda : negative)) | bge & Not(Defer(1,lambda : negative))

    
    jump = jal 
    
    branch_or_jump = branching|jump

    #jvalue = adder(Mux(jump,immBtype[5:],immJtype[13:]),Constant("0000010"),Constant("0"),None)[0]
    jvalue = Mux(jump,immBtype[4:],immJtype[12:])[:7]

    #binop entre deux regs
    add = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0000000"))
    sub = valopcode[51] & eq(funct3,Constant("000")) & eq(funct7,Constant("0100000")) | beq | bneq | blt | bge
    orbinop= valopcode[51] & eq(funct3,Constant("110")) & eq(funct7,Constant("0000000"))
    andbinop = valopcode[51] & eq(funct3,Constant("111")) & eq(funct7,Constant("0000000"))
    xor = valopcode[51] & eq(funct3,Constant("100")) & eq(funct7,Constant("0000000"))
    slt = valopcode[51] & eq(funct3,Constant("010")) & eq(funct7,Constant("0000000"))
    sltu = valopcode[51] & eq(funct3,Constant("011")) & eq(funct7,Constant("0000000"))
    op_entre_deux_reg = add | sub | orbinop| andbinop | xor |slt |sltu

    #binop entre regs et imm

    addi = valopcode[19] & eq(funct3,Constant("000"))
    xori = valopcode[19] & eq(funct3,Constant("100"))
    ori = valopcode[19] & eq(funct3,Constant("110"))
    andi = valopcode[19] & eq(funct3,Constant("111"))

    
    
    op_entre_reg_et_i = addi | xori | ori | andi

    ##mémoire

    lw = valopcode[3] & eq(funct3,Constant("010"))
    sw = valopcode[35] & eq(funct3,Constant("010"))





    load = lw
    store = sw

    ##

    waddr = rd 
    raddr1 = rs1 
    raddr2 = rs2 


    op = op_entre_deux_reg | op_entre_reg_et_i | load | store
    wenable = op_entre_deux_reg | load | lui |op_entre_reg_et_i | load

    rdata1,rdata2 = regblock(waddr,Defer(32,lambda:wdata),wenable,raddr1,raddr2)

    allowin1 = op
    

    inalu1 = Mux(allowin1,zero,rdata1)
    inalu2 = Mux(store,Mux(load,Mux(op_entre_reg_et_i,Mux(op_entre_deux_reg,zero,rdata2),Constant("0"*20)+immItype),Constant("0"*20)+ immItype),Constant("0"*20)+immStype)
    
    vsub = (sub |slt |sltu|beq |bge |blt |bneq) & op_entre_deux_reg 
    vnot = op_entre_deux_reg & Constant("0")
    vand = (op_entre_deux_reg & andbinop) | (op_entre_reg_et_i & andi)
    vor = (op_entre_deux_reg & orbinop) | (op_entre_reg_et_i & ori)
    vxor = (op_entre_deux_reg & xor) | (op_entre_reg_et_i & xori)

    (outalu,overflow,negative,null) = alu(inalu1,inalu2,vsub,vnot,vand,vor,vxor,32)

    ramWenable = store
    ramRaddr = Mux(load,zero,outalu)[24:]
    ramWaddr = Mux(store,zero,outalu)[24:]
    ramWdata = rdata2

    ramdata = RAM(8,32,ramRaddr,ramWenable,ramWaddr,ramWdata)
    
    
    wdata = Mux(lui,Mux(load,Mux(jump,Mux(slt|sltu,outalu,zero[:31] + negative),Constant("0"*25) + incroffset),ramdata),Constant("0"*12) + immJtype)



    return offset,instr,jvalue,branch_or_jump

def main():
    x = Input(0)
    a = processeur()
    a[0].set_as_output("out")
    a[1].set_as_output("instruction")
    a[2].set_as_output("jval")
    a[3].set_as_output("j")
    