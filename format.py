import sys


path = sys.argv[1]

fichier = open(path,"r")
output = open("output.txt","w")
    

l = fichier.readlines()


for x in l:
    y = x.split(" ")
    s = y[4] + y[3] + y[2] + y[1]
    output.write(s+"\n")

for i in range(128):
    output.write("0"*32 + "\n")

output.close()
fichier.close()