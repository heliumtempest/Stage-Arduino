from datetime import timedelta
from Capteurs.CapteurInterface import CapteurInterface as GenCap


class Capteur(GenCap):
    """Classe qui représente le capteur DHT22 qui mesure la température et l'humidité et calcule également l'indice de
    chaleur (température ressentie)."""

    def __init__(self):
        super().__init__()
        # Emplacement (de manière relative) du fichier csv à générer qui contiendra les données reçues
        self.chemin_csv = "Capteurs/DHT22/csv/DHT_22" + self.t0_str + ".csv"
        self.requete_insertion = "INSERT INTO DHT22(Session, Date, Humidite, Temperature, Indice) " \
                                 "VALUES ('{s}', '{dm}', {h}, {t}, {i});"
        self.affichage_console = "Humidité : {h}, Temperature : {t}, Indice : {i}, T0+{tec} ms "

        # Création et écriture de l'entête du fichier csv
        entete = "Humidite;Temperature;Indice de chaleur;Tecoule\n"
        csv = open(self.chemin_csv, 'a')
        csv.write(entete)
        csv.close()

    def afficher_console(self, ligne):
        """Affiche pour chaque ligne lue le message à faire apparaître dans la console"""
        # Séparation des différents champs de la ligne lue
        donnees = ligne.split(" ")
        # Formatage de la chaîne de caractère pour y insérer les valeurs récupérées provenant du capteur
        affichage = self.affichage_console.format(
            h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]), tec=int(donnees[3]))
        # Affichage dans la console
        print(affichage)

    def inserer_bdd(self, ligne):
        """Insère un enregistrement dans la base de données qui correspond à la ligne lue"""
        donnees = ligne.split(" ")
        # Calcul de la date de la mesure
        # ( = date de la 1ère mesure + temps écoulé depuis l'execution du programme arduino)
        timestamp = self.t0 + timedelta(milliseconds=int(donnees[3]))
        # Création et execution de la requête SQL
        requete = self.requete_insertion.format(h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]),
                                                dm=timestamp, s=self.bdd.nom_session)
        self.bdd.executer_requete(requete)

    def ecrire_csv(self, ligne):
        """Écrit une ligne dans le fichier csv qui correspond à la ligne lue depuis le capteur."""
        # Attention : ouvrir le fichier pendant son écriture générera une erreur
        # Récupérer les données sous forme d'une liste
        donnees = ligne.split(" ")
        separateur_csv = ";"
        # Ouverture en mode 'append' pour ne pas écraser le contenu du fichier à chaque appel de la méthode
        fichier = open(self.chemin_csv, 'a')
        fichier.write(separateur_csv.join(donnees) + "\n")
        fichier.close()

    def creer_table(self):
        """Execute le script qui correspond à la création de la table contenant les mesures du capteurs dans la base de
        données."""
        # Lecture du fichier contenant le script
        try:
            script = open("Capteurs/DHT22/table_DHT22.sql", "r")
        except FileNotFoundError:
            print("Script de création non trouvé")
            exit()
        # Execution du script
        self.bdd.executer_requete(script.read())
