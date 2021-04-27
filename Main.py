import os
os.chdir("C:\\Users\\ghisl\\PycharmProjects\\Arduino") #TODO mettre 'here'(__file__) comme wd ?
# En fait, pas nécessaire, mais on peut tojours mettre les points sur les i
# Edit : c'est nécessaire si on l'execute en dehors de l'emplacement où il y a tout le reste du projet
  
try:
    import Commun.ConnexionPostgres as pg
    import Commun.Port as pt
except ModuleNotFoundError:
    print("Les modules n'ont pas été détectés, vérifier l'emplacement des fichiers")
    exit()

print("Voulez-vous utiliser les paramètres par défaut de connexion de la BDD :")
utilisateur = pg.ConnexionPostgres()
utilisateur.defaut_param()
utilisateur.afficher_info()
while True:
    reponse = input("Oui(O) ou Non(N) : ")
    if(reponse == "O" or reponse == "o"):
        break  # Ne rien modifier et sortir de la boucle
    elif(reponse == "N" or reponse == "n"):
        utilisateur.saisie_param()
        break  # Sortir de la boucle
    else:
        #print("g pa konpri")
        print("Réponse non reconnue")

# Vérifie la validité de la connexion
utilisateur.connexion_bdd()
# Demande de saisie du nom de la session
utilisateur.saisir_nom_session()

# Lecture du port
port = pt.Port()
port.selectionner_port()
port.lire_port()
