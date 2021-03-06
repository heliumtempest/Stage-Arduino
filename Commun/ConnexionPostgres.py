try:
    # Le module psycopg2 n'est pas présent dans les modules fournis de base et doit être installé
    import psycopg2
except ModuleNotFoundError:  # Le module n'est pas installé
    # Installation automatique du module
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2"])


# TODO nettoyer les commmentaires à l'occasion
class ConnexionPostgres:
    # """Classe qui contient les différentes informations de connexion vers la base de données où seront insérées les
    # mesures rélisées par les capteurs. """

    # Attributs statiques
    # Rq : il est possible d'accéder à ces attributs par une instance, ou par la classe elle-même
    serveur = ""  # Adresse IP du serveur
    utilisateur = ""
    mot_de_passe = ""
    base_de_donnees = ""
    nom_session = "" # TODO trouber un nom de session potentiellement intéressant par défaut QUOIQUE param != nom de session

    def saisie_param(self):
        """Permet à l'utilisateur de saisir les différents paramètres de connexion."""
        # Modification des attributs statiques
        ConnexionPostgres.serveur = input("Adresse du serveur : ")
        ConnexionPostgres.utilisateur = input("Nom de l'utilisateur : ")
        ConnexionPostgres.mot_de_passe = input("Mot de passe : ")  # Un mdp devrait pas être en clair mais tant pis
        ConnexionPostgres.base_de_donnees = input("Nom de la base de données : ")

    def defaut_param(self):
        """Initialise les informations de connexion à des valeurs par défaut."""
        # Modification des attributs statiques
        ConnexionPostgres.serveur = "127.0.0.1"
        ConnexionPostgres.utilisateur = "postgres"
        ConnexionPostgres.mot_de_passe = "admin"
        ConnexionPostgres.base_de_donnees = "arduino"

    def saisir_nom_session(self):
        """Demande à l'utilisateur de saisir le nom de la session de mesure, afin de compléter le champ associé dans
         la base de données."""
        # TODO (c'est jsute une petite remarque)
        # La saisie du nom de session ne sefait pas au niveau des autres paramètres, puisque ça n'a rien à voir avec
        # et la connexion est d'abord testée avant de demander le nom de session
        ConnexionPostgres.nom_session = input("Nom de la session de mesure : ")

    def connexion_bdd(self):
        """Initialise une connexion vers la base de données"""
        # Rq : database n'est pas un paramètre nécéssaire pour une connexion
        # Rq2 : la connexion semble se faire même si le serveur n'est pas démarré (wow!)
        try:
            connexion = psycopg2.connect(
                host=ConnexionPostgres.serveur,
                user=ConnexionPostgres.utilisateur,
                password=ConnexionPostgres.mot_de_passe,
                database=ConnexionPostgres.base_de_donnees
            )
            return connexion
        except psycopg2.OperationalError:
            print("Échec de la connexion à la base de données")
            print("Verifier les paramètres de connexion")
            exit()

    def executer_requete(self, requete_sql):
        """Utilise une connexion afin d'executer une requête SQL sur la base de données."""
        #Rq : Je crois que ça ne peut executer qu'une seule requête, il y a une erreur s'il y en a plusieurs
        # Établissement d'une connexion avec la abse de données
        connexion = self.connexion_bdd()
        # Rq : Il y a une gestion d'exception pour la fonction connexion_bdd
        # Éxécution de la requête
        try:
            curseur = connexion.cursor()
            curseur.execute(requete_sql)
            connexion.commit()
            curseur.close()
            connexion.close()
        #except psycopg2.OperationalError:
        except psycopg2.errors.SyntaxError as err:
            print("Erreur de syntaxe au niveau de la requête")
            print("La requête était : ", requete_sql)
            print(str(err))
            # TODO c'est un peu lourd au niveau affichage de la console
        except psycopg2.errors.UndefinedColumn:
            print("Nom de colonne non reconnu. La requête était :\n", requete_sql)
            # Une cause possible est l'absence de " autour des noms de la colonnes (cf. script de création de table)
        except:
            print("Echec le l'execution de la requete")
            print("La requête était : ", requete_sql)
            raise
        #TODO : psycopg2.OperationalError (je crois que ça m'est arrivé lorsqu'aucune BDD n'était dispo)
        #TODO : erreur bloquante ou non ?

    def afficher_info(self):
        """Affiche les différentes informations de connexion dans la console."""
        print("Serveur :", ConnexionPostgres.serveur)
        print("Utilisateur :", ConnexionPostgres.utilisateur)
        print("Mdp :", ConnexionPostgres.mot_de_passe) #TODO le joli mdp en clair (est-ce grave pour autant dans notre contexte)
        print("BDD :", ConnexionPostgres.base_de_donnees)

