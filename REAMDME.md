




Utilisation de carotte : 

python3 ./carotte/carotte.py *chemin vers la netlist en . py"

python3 ./carotte/carotte.py *chemin vers la netlist en . py" > "chemin vers l'output souhaitée"

exemple : 

cd ./carotte
python3 ./carotte.py ./processeur/ndemux.py > ./processeur/ndemux.net






Pour tester des netlists :

./tp1/netlist_simulator.byte *chemin vers la netlist*








Pour assembler des fichiers de code en RISCV vers un fichier .txt contenant du binaire (doc : https://www.riscvassembler.org/index.html): 

pip install riscv-assembler


python3 ./riscvprog/convertir.py  *chemins vers les fichiers assembly en .s à convertir*

python3 ./riscvprog/convertir.py ./riscvprog/test.s




Modification du simulateur :

On autorise la logique de ruban
Le comportement du mux est cohérent 

Les registres sont maitentant initialisé à la bonne taille

