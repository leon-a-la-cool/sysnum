from riscv_assembler.convert import AssemblyConverter 
from sys import argv

cnv = AssemblyConverter(output_type="t")


for i in range(1,len(argv)):
    
    cnv.convert(argv[i])

    