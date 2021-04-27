from datetime import datetime, timedelta
from Capteurs.CapteurInterface import CapteurInterface as GenCapt  # Pour CapteurGeneral

class Capteur(GenCapt):

    def __init__(self):
        super().__init__()  # Appel du constructeur (__init__) de l'interface
        self.requete = "INSERT INTO TSL2561(\"Session\",\"Lux\", \"LuminositeIR\", \"Luminosite\", \"DateMesure\") " \
                       "VALUES ('{S}', {L}, {IR}, {Lum}, '{ts}');"
        # Requête SQL (à formater) pour ajouter un enregistrement dans la base de données
        # Des " autour des noms de colonnes sont nécessaires dans la requête SQL (cf. le script de création de la table)

        # Nom du fichier .csv à créer (nom capteur + date et heure du jour)
        self.chemin_csv = "Capteurs/TSL2561/csv/TSL2561_" + datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S') + ".csv"
        # Le timestamp est formaté (les ':' dans le timestamp initial ne peuvent être utilisé dans un nom de fichier)

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
        # Préparation de la requête
        sql = self.requete.format(S=self.bdd.nom_session, L=int(donnees[0]), IR=int(donnees[1]), Lum=int(donnees[2]),
                                  ts=timestamp)
        # Execution de la requête
        self.bdd.executer_requete(sql)

    def ecrire_csv(self, ligne):
        """Formate une ligne reçue du capteur afin de l'écrire dans le fichier csv"""
        csv = open(self.chemin_csv, 'a')
        csv.write(ligne.replace(" ", ";") + "\n")  # Convertit les espaces dans la ligne lue par des ; et ajoute un saut de ligne en fin de ligne
        csv.close()

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
        #TODO mettre dans le try ? (je sais pas ce que ça va faire niveau gestion d'exception)
        self.bdd.executer_requete(script_sql)
