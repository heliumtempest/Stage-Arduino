import psycopg2

# TODO nettoyer les commmentaires à l'occasion
class ConnexionPostgres:

    serveur = ""
    utilisateur = ""
    mot_de_passe = ""
    base_de_donnees = ""

    def saisie_param(self):
        """Permet à l'utilisateur de saisir les différents paramètres de connexion"""
        self.serveur = input("Adresse du serveur : ")
        self.utilisateur = input("Nom de l'utilisateur : ")
        self.mot_de_passe = input("Mot de passe : ")  # Un mdp devrait pas être en clair mais tant pis
        self.base_de_donnees = input("Nom de la base de données : ")

    def defaut_param(self):
        """Initialise les informations de connexion à des valeurs par défaut"""
        self.serveur = "127.0.0.1"
        self.utilisateur = "postgres"
        self.mot_de_passe = "admin"
        self.base_de_donnees = "arduino"

    def connexion_bdd(self):
        """Initialise une connexion vers la base de données"""
        # Rq : database n'est pas un paramètre nécéssaire pour une connexion
        # Rq2 : la connexion semble se faire même si le serveur n'est pas démarré (wow!)
        try:
            connexion = psycopg2.connect(
                host=self.serveur,
                user=self.utilisateur,
                password=self.mot_de_passe,
                database=self.base_de_donnees
            )
            #print("Connexion effectuée")
            return connexion
        except psycopg2.OperationalError:
            print("Échec de la connexion à la base de données")
            print("Verifier les paramètres de connexion")
            exit()

    def executer_requete(self, requete_sql):
        """Utilise une connexion afin d'executer une requête SQL sur la base de données"""
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
        except:
            print("Echec le l'execution de la requete")
            print("La requête était : ", requete_sql)
            raise
        #TODO : cas d'une colonne n'éxistant pas : psycopg2.errors.UndefinedColumn


    # TODO un autre intérêt que le débug ?
    def afficher_info(self):
        """Affiche les différentes informations de connexion"""
        print("Serveur :", self.serveur)
        print("Utilisateur :", self.utilisateur)
        print("Mdp :", self.mot_de_passe) #TODO le joli mdp en clair
        print("BDD :", self.base_de_donnees)

