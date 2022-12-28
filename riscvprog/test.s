init:
    addi x2,x2,3

main: 
    addi x1, x1, 1
    sw x1, 1(x0)
    beq x1,x2,init
    addi x1, x1, 1
    jal x0,main

