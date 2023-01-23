
main:
    addi x4,x4,1
    sw x4,2(x0)
    sub x4,x4,x4
    addi x4,x4,3
    sw x4, 1(x0)
    lui x3,234
    