lui x3,1

main2:
    addi x3,x3,1
    addi x3,x8,0
    sw x8,2(x0)
    ecall
    sw x8,2(x0)
    
    lw x13, 9(x0)
    xori x13,x13,1
    sw x13, 9(x0)
    jal x0,main2

