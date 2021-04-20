from datetime import datetime, timedelta


class Capteur:

    def __init__(self, **kwargs):
        # TODO donner la possibilité de passer la bdd en param du constructeur (quoique?
        self.bdd = None  # Indique la connexion vers la base de données (à affecter après l'instanciation de l'objet)
        self.t0 = datetime.now()  # Timestamp
        self.requete = "INSERT INTO TSL2561(\"Lux\", \"LuminositeIR\", \"Luminosite\", \"DateMesure\") " \
                       "VALUES ({L}, {IR}, {Lum}, {ts})"
        # Requête SQL (à formater) pour ajouter un enregistrement dans la base de données
        # Des " autour des noms de colonnes sont nécessaires dans la requête SQL (cf. le script de création de la table)

        # Nom du fichier .csv à créer (nom capteur + date et heure du jour)
        self.chemin_csv = "Capteurs/TSL2561/csv/TSL2561_" + datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S') + ".csv"
        # Le timestamp est formaté (les ':' dans le timestamp initial ne peuvent être utilisé dans un nom de fichier)
        # Il n'est donc pas possible d'utiliser str(t0)

        # Création du fichier et écriture de l'entête
        header = "Lux;LumIR;Lum;Tec\n"
        csv = open(self.chemin_csv, 'a')
        csv.write(header)
        csv.close()

    def afficher_console(self, ligne):
        champs = ligne.split(" ")
        affichage = "Lux : {L}, Luminosité (IR) : {IR}, Luminosité (Spectre entier) : {SE}, T0+{ms}ms".format(
            L=champs[0], IR=champs[1], SE=champs[2], ms=champs[3])
        print(affichage)

    def inserer_bdd(self, ligne):
        # Lecture des données reçues
        donnees = ligne.split(" ")
        # Calcul du 'timestamp' (temps initial (t0) + temps écoulé)
        timestamp = self.t0 + timedelta(milliseconds=int(donnees[3]))
        timestamp = "'{}'".format(timestamp)  # Formatage pour la requête
        # Préparation de la requête
        sql = self.requete.format(L=int(donnees[0]), IR=int(donnees[1]), Lum=int(donnees[2]), ts=timestamp)
        # Execution de la requête
        self.bdd.executer_requete(sql)

    def ecrire_csv(self, ligne):
        # TODO décommenter la fonction (je veux juste éviter de créer un csv à chaque fois)
        # """Formate une ligne reçue du capteur afin de l'écrire dans le fichier csv"""
        # csv = open(self.chemin_csv, 'a')
        # csv.write(ligne.replace(" ", ";") + "\n")  # Convertit les espaces dans la ligne lue par des ; et ajoute un saut de ligne en fin de ligne
        # csv.close()
        return

    def creer_table(self):
        """Execute le script de création de la base de données"""
        # Cette méthode est systematiquement éxécutée après l'importation du module
        try:
            # Ouvre le fichier contenant le script à l'emplacement scpécifié
            fichier_script = open("Capteurs/TSL2561/table_tsl2561.sql", 'r')
            # Récupération du contenu du fichier
            script_sql = fichier_script.read()
        except FileNotFoundError:  # Le script n'est pas à l'emplacement spécifié
            print("Script de création de la table introuvable")
            exit()

        # Execution du script
        # Rq : il y a une gestion d'exception dans la méthode executer_requete()
        self.bdd.executer_requete(script_sql)
