Pour compiler : ./compile


Pour exécuter l'horloge : ./horloge <vitesse> <date intiale>
    valeurs possibles : 
        <vitesse>: -slow : vitesse réelle
                   -fast : vitesse maximale
                   -day : vitesse maximale sur les jours
        <date initiale>: -cuurentdate : date initiale actuelle
                        non spécifiée : 01/01/0000 0h0min0s




Utilisations plus spécifiques :
    Pour assembler au bon format : ./assembler <fichier.s> <sortie.txt>
    Simulateur: ./simulateur/netlist_simulator.byte -r <programme cible.txt> <chemin vers la netlist du processeur>  
            avec comme arguments facultatifs : -fullspeed : vitesse maximale (ne pas préciser pour synchronisation avec temps réel)
                                               -flip : tout le temps afficher (ne pas préciser pour attendre le signal du processeur)
                                               -nodisplay : afficher dans la console et ne pas transmettre au programme python
                                               -currentdate : se synchroniser avec la date actuelle (ne rien mettre pour commencer à 0)