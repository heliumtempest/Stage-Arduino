import psycopg2

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
        # TODO try/except
        # Rq : database n'est pas un paramètre nécéssaire
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
            exit()


    def executer_requete(self, requete_sql):
        """Utilise une connexion afin d'executer une requête SQL sur la base de données"""
        #Rq : Je crois que ça ne peut executer qu'une seule requête, il y a une erreur s'il y en a plusieurs

        connexion = self.connexion_bdd()
        #Rq : j'ai déjà un try/except dans la fonction de connexion
        try:
            curseur = connexion.cursor()
            curseur.execute(requete_sql)
            connexion.commit()
            connexion.close()
        except:
            print("Echec le l'execution de la requete")
            raise

# TODO effacer ces petits tests à l'occasion
# utilisateur = PostgresDAO()
# utilisateur.defaut_param()
# utilisateur.connexion_bdd()
