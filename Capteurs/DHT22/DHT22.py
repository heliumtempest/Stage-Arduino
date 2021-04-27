from datetime import datetime, timedelta
from Capteurs.CapteurInterface import CapteurInterface as GenCap


# Classe qui représente le DHT22
# (les classes des capteurs vont toutes avoir le même nom, ça rend leur appel facile)
# (c'est comme des implémentation d'une même interface) => c'est désormais le cas
class Capteur(GenCap):

    def __init__(self):
        super().__init__()  # La connexion vers la BDD est récupérée depuis l'interface
        # Date de la mesure initiale (t0 est initialisé une seule fois lors de la création de l'instance)
        self.chemin_csv = "Capteurs/DHT22/csv/DHT_22" + self.t0_str + ".csv"
        # self.requete_insertion = "INSERT INTO DHT22(Temperature, Humidite, DateMesure, Indice) " \
        #                          "VALUES ({t}, {h}, {dm}, {i});"
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
        # affichage = "Humidité : {h}, Temperature : {t}, Indice : {i}, T0+{tec} ms ".format(
        #     h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]), tec=int(donnees[3]))
        #TODO j'ai fait une petite modification, à tester
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
        # Création de la requête SQL
        requete = self.requete_insertion.format(h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]),
                                                dm=timestamp, s=self.bdd.nom_session)
        self.bdd.executer_requete(requete)

    def ecrire_csv(self, ligne):
        """Écrit une ligne dans le fichier csv qui correspond à la ligne lue depuis le capteur"""
        # Attention : ouvrir le fichier pendant son écriture générera une erreur

        ligne = ligne.split(" ")
        separateur_csv = ";"  # C'est plus explicite
        # # Conversion timestamp -> str (afin de l'utiliser pour nommer le fichier)
        # date = datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S')
        # Ouverture en mode 'append' pour ne pas écraser le contenu du fichier à chaque appel de la méthode
        #fichier = open("Capteurs/DHT22/csv/DHT22_" + date + ".csv", 'a')
        fichier = open(self.chemin_csv, 'a')
        fichier.write(separateur_csv.join(ligne) + "\n")
        # Fermeture du fichier
        fichier.close()
        # TODO moi et mes commentaires...
        # edit : en pratique pas nécessaire (mais je trouve que c'est plus propre)

    def creer_table(self):
        # Lecture du fichier contenant le script
        #TODO enlever les print de debug
        try:
            script = open("Capteurs/DHT22/table_DHT22.sql", "r")
            #print("Script trouvé")
        except FileNotFoundError:
            print("Script de création non trouvé")
            exit()
        # Execution du script
        self.bdd.executer_requete(script.read())
        #print("Table créée")

    # TODO nettoyer les commentaires
    # def parser_ligne(self, ligne):
    #     """Convertit la ligne de texte reçue par le port avec les données correspondantes"""
    #     # Ce n'est pas une méthode nécessaire à implémenter mais elle est pratique
    #     champs = ligne.split(" ")
    #     data = [float(champs[0]), float(champs[1]), float(champs[2]), int(champs[3])]
    #     # (humidité, température, indice de chaleur, temps écoulé)
    #     return data
    # # Pas sûr qu'elle aide tant que ça, puisque je sais pas si on peut remplacer des {} dans des str à l'aide d'une liste

#print("Hello de DHT22")
