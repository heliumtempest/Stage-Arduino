import os
os.chdir("C:\\Users\\ghisl\\PycharmProjects\\Arduino") #TODO mettre 'here'(__file__) comme wd ?
# En fait, pas nécessaire, mais on peut tojours mettre les points sur les i
# Edit : c'est nécessaire si on l'execute en dehors de l'emplacement où il y a tout le reste du projet

# Rq : le module "psycopg2" doit être installé
# TODO le faire dans leur module respectif
try:
    # Ce module n'est pas présent dans les modules de base de python et doit être installé
    import psycopg2
    #import serial.tools.list_ports
except:
    # S'il n'est pas présent, l'installer
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2"])
    #subprocess.check_call([sys.executable, "-m", "pip", "install", "serial.tools.list_ports"])
    #Il me semble que c'était 'pyserial' qu'il fallait installer
  
try:
    import Commun.ConnexionPostgres as pg
    import Commun.Port as pt
except:
    print("L'import des modules a échoué")
    input("Appuyer sur une touche pour continuer")
    exit()

print("Voulez-vous utiliser les paramètres par défaut de connexion de la BDD :")
utilisateur = pg.ConnexionPostgres()
utilisateur.defaut_param()
utilisateur.afficher_info()
reponse = input("Oui (O) ou Non(N) : ")
if(reponse == "O" or reponse == "o"):
    #utilisateur.defaut_param()
    pass  # ne rien modifier
elif(reponse == "N" or reponse == "n"):
    utilisateur.saisie_param()
else:
    #print("g pa konpri")
    print("Réponse non reconnue")
    #input()
    exit()

# Vérifie la validité de la connexion
utilisateur.connexion_bdd()
# Demande de saisie du nom de la session
utilisateur.saisir_nom_session()

# Lecture du port
port = pt.Port()
port.selectionner_port()
port.lire_port()
