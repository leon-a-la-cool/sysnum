

POUR COMPILER DES FICHIERS AVEC CAROTTE il faut travailler sur des fichiers dans le meme dossier jsp comment faire autrement c'est python 
Ca veut dire qu'il faut déplacer le dossier processeur dans le dossier carotte c'est tout voilà on peut pas le faire sur la version git parce que le depot carotte est protegé jsp quoi


Utilisation de carotte : 

python3 ./carotte/carotte.py *chemin vers la netlist en . py"

python3 ./carotte/carotte.py *chemin vers la netlist en . py" > "chemin vers l'output souhaitée"

exemple : 

cd ./carotte
python3 ./carotte.py ./processeur/ndemux.py > ./processeur/ndemux.net








Pour assembler des fichiers de code en RISCV vers un fichier .txt contenant du binaire :
Utiliser le script assembler:
./assembler ./riscvprog/test.s ./test.txt
./assembler "chemin du .s à assembler" "chemin vers le fichier .txt produit"





Processeur 16 registres de 16 bits

Les programmes ont au maximum 128 instr
la RAM a 256 addressses diff



Instructions set :

BEQ,BNE,BLT,BGE
ADDI,XORI,ORI,ANDI
ADD,SUB,XOR,AND,OR
JAL
LUI, LW, SW







Modification du simulateur :

On autorise la logique de ruban
Le comportement du mux est cohérent 

Les registres sont maitentant initialisé à la bonne taille

Les adresses memoire de la ram 1,2,3,4,5,6 sont affichées, le simulateur crash sur une netlist sans ram

Il faut donner via l'argument -r le programme à exécuter.

Utiliser -fullspeed pour vitesse maximale





Quand on ecall, x8 est converti en 7seg, envoyé dans x8 