lui x5,1
lui x4,1

main:
    lw x14,(x0)
    bne x15,x14,main2
    jal x0,main


display_flip:
    addi x8,x1,0
    ecall
    sw x8, 1(x0)
    addi x8,x2,0
    ecall
    sw x8, 2(x0)
    addi x8,x3,0
    ecall
    sw x8, 3(x0)
    addi x8,x4,0
    ecall
    sw x8, 4(x0)
    addi x8,x5,0
    ecall
    sw x8, 5(x0)
    addi x8,x6,0
    ecall
    sw x8, 6(x0)
    addi x8,x7,0
    ecall
    sw x8, 7(x0)
    lw x13, 9(x0)
    xori x13,x13,1
    sw x13, 9(x0)
    jal x0,main

main2:
    xori x15,x15,1
    lui x13, 59
    beq x1, x13, sec_reset
    addi x1, x1, 1
    jal x0,display_flip


#x1,x2,x3,x4,x5,x6,x7 = sec min hr jr mois andizaine anmillier 
#x13 = travail
#x14,x15 = clock
#x11 = parité mois
#x10 = bisextile
bisextile_reset:
    sub x10,x10,x10
    lui x13,100
    beq x6,x13,decade_reset
    jal x0,main


decade_reset:
    lui x6,0
    addi x7,x7,1
    jal x0,display_flip




mounth_reset:
    lui x5,1
    lui x4,1
    addi x6,x6,1
    addi x10,x10,1
    lui x13,4
    beq x10,x13,bisextile_reset
    jal x0,display_flip

day_reset:
    lui x4,1
    xori x11,x11,1
    addi x5,x5,1
    lui x13,13
    beq x13,x5,mounth_reset
    jal x0,display_flip


feb_bis:
    lui x13,30
    beq x13,x4,day_reset
    jal x0,display_flip
feb_normal:
    lui x13,29
    beq x13,x4,day_reset
    jal x0,display_flip
feb:
    lw x10, 10(x0) #bisextile 
    lui x13,0
    beq x10,x13,feb_bis
    jal x0,feb_normal
shortmonth:
    lui x13,31
    beq x4,x13,day_reset
    jal x0,display_flip
longmonth:
    lui x13,32
    beq x4,x13,day_reset
    jal x0,display_flip
augdec:
    lui x13,0
    beq x13,x11,longmonth
    jal x0,shortmonth
janjul:
    lui x13,1
    beq x13,x11,longmonth
    jal x0,shortmonth


hr_reset:
    lui x3,0
    addi x4,x4,1
    lui x13, 2
    beq x13, x5, feb
    lui x13, 7
    ble x5,x13,janjul
    jal x0,augdec


min_reset:
    lui x2,0
    addi x3,x3, 1
    lui x13,24 #24
    beq x3,x13, hr_reset
    jal x0,display_flip


sec_reset:
    lui x1,0
    addi x2,x2, 1 
    lui x13, 60 #60
    beq x2,x13, min_reset
    jal x0,display_flip
    

