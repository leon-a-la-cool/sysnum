addi x5,x5,60
addi x6,x6,24
addi x7,x7,365



main: 
    addi x1, x1, 1
    beq x1, x5, sec_reset
    sw x1, 0(x0)
    sw x2, 1(x0)
    sw x3, 2(x0)
    sw x4, 3(x0)
    jal x0,main


hr_reset:
    sub x3,x3,x3
    addi x4,x4,1
    jal x0,main


min_reset:
    sub x2, x2, x2
    addi x3,x3, 1
    beq x2,x6, hr_reset
    jal x0,main


sec_reset:
    sub x1, x1, x1
    addi x2,x2, 1 
    beq x2,x5, min_reset
    jal x0,main
    
