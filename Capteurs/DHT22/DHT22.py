from datetime import datetime, timedelta

# Classe qui représente le DHT22
# (les classes des capteurs vont toutes avoir le même nom, ça rend leur appel facile)
# (c'est comme des implémentation d'une même interface)
class Capteur():

    # Connexion vers la BDD (bdd est une instance de ConnexionPostgres)
    bdd = None
    # Date de la mesure initiale (t0 est initialisé une seule fois lors de la création de l'instance)
    t0 = datetime.now()

    # TODO tester la nouvelle version avec le chemin en attribut
    chemin_csv = "Capteurs/DHT22/csv/DHT_22" + datetime.strftime(t0, '%Y-%m-%d_%H-%M-%S') + ".csv"
    # Écriture du header
    fichier = open(chemin_csv, 'a')
    fichier.write("Humidite;Temperature;Indice de chaleur;Tecoule")
    fichier.close()

    def __init__(self):
        # TODO tester si ça marche (notamment pour le csv)
        self.bdd = None
        self.t0 = datetime.now()
        self.chemin_csv = "Capteurs/DHT22/csv/DHT_22" + datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S') + ".csv"

        # Création et écriture de l'entête du fichier csv
        entete = "Humidite;Temperature;Indice de chaleur;Tecoule"
        csv = open(self.chemin_csv, 'a')
        csv.write(entete)
        csv.close()

    def afficher_console(self, ligne):
        """Affiche pour chaque ligne lue le message à faire apparaître dans la console"""
        # Séparation des différents champs de la ligne lue
        donnees = ligne.split(" ")
        # Formatage de la chaîne de caractère pour y insérer les valeurs récupérées provenant du capteur
        affichage = "Humidité : {h}, Temperature : {t}, Indice : {i}, T0+{tec} ms ".format(
            h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]), tec=int(donnees[3]))
        # Affichage dans la console
        print(affichage)

    def inserer_bdd(self, ligne):
        """Insère un enregistrement dans la base de données qui correspond à la ligne lue"""
        donnees = ligne.split(" ")
        # Calcul de la date de la mesure
        # ( = date de la 1ère mesure + temps écoulé depuis l'execution du programme arduino)
        timestamp = self.t0 + timedelta(milliseconds=int(donnees[3]))
        # Sur Postgres, les timestamps doivent être mis entre quotes
        timestamp = "'{0}'".format(timestamp)
        # Création de la requête SQL
        requete = "INSERT INTO DHT22(Temperature, Humidite, DateMesure, Indice) VALUES ({t}, {h}, {dm}, {i});".format(
            h=float(donnees[0]), t=float(donnees[1]), i=float(donnees[2]), dm=timestamp)
        # Faudrait plutôt mettre le try/except dans la méthode executer_requete
        try:
            self.bdd.executer_requete(requete)
        except:
            print("Echec de la connexion depuis l'insertion")
            # Afficher la requête afin de pouvoir tester son execution sur Postgres
            print("La requête était : ", requete)

    def ecrire_csv(self, ligne):
        """Écrit une ligne dans le fichier csv qui correspond à la ligne lue depuis le capteur"""
        # TODO j'ai un peu rectifié la fonction afin d'avoir le chemin en attribut
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
        # edit : en pratique pas nécessaire

    def creer_table(self):
        # Lecture du fichier contenant le script
        try:
            script = open("Capteurs/DHT22/table_DHT22.sql", "r")
            print("Script trouvé")
        except FileNotFoundError:
            print("Script de création non trouvé")
            exit()
        # Execution du script
        self.bdd.executer_requete(script.read())
        print("Table créée")


    # def parser_ligne(self, ligne):
    #     """Convertit la ligne de texte reçue par le port avec les données correspondantes"""
    #     # Ce n'est pas une méthode nécessaire à implémenter mais elle est pratique
    #     champs = ligne.split(" ")
    #     data = [float(champs[0]), float(champs[1]), float(champs[2]), int(champs[3])]
    #     # (humidité, température, indice de chaleur, temps écoulé)
    #     return data
    # # Pas sûr qu'elle aide tant que ça, puisque je sais pas si on peut remplacer des {} dans des str à l'aide d'une liste

#print("Hello de DHT22")
