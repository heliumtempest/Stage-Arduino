import Capteurs.CapteurInterface as ci
import Capteurs.TSL2561.TSL2561 as tsl
import Capteurs.DHT22.DHT22 as dht
import Capteurs.Cardio.Cardio as car


class Capteur(ci.CapteurInterface):

    def __init__(self):
        # Utilisation du constructeur de l'interface pour
        super(Capteur, self).__init__()
        # Instanciation des classes de chacun des capteurs
        self.dht = dht.Capteur()
        self.tsl = tsl.Capteur()
        self.car = car.Capteur()

    def creer_table(self):
        # Chaque objet qui représente capteur crée la table qui lui associée
        self.dht.creer_table()
        self.tsl.creer_table()
        self.car.creer_table()

    def ecrire_csv(self, ligne):
        # TODO le path
        # TODO faire ça proprement (header, etc)
        # L'ensemble des mesure est
        path = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\trio_{t0}.csv".format(t0=self.t0_str)
        csv = open(path, 'a')
        csv.write(ligne.replace(' ', ';') + "\n")
        csv.close()

    def inserer_bdd(self, ligne):
        # Séparation des différents champs de la ligne lue
        donnees = ligne.split(" ")
        ms = donnees[7]  # Temps écoulé depuis l'execution du programme ardduino en millisecondes

        # 'Reconstruction' de la ligne qui aurait été reçue s'il y avait seulement le capteur Cardio
        # afin d'employer la méthode de la classe associée pour l'insertion des données dans la base de données
        donnes_car = donnees[0]
        donnes_car += ' ' + ms
        self.car.inserer_bdd(donnes_car)

        # 'Reconstruction' de la ligne qui aurait été reçue s'il y avait seulement le capteur DHT22
        # afin d'employer la méthode de la classe associée pour l'insertion des données dans la base de données
        donnes_dht = donnees[1:4]
        donnes_dht.append(ms)
        self.dht.inserer_bdd(' '.join(donnes_dht))

        # 'Reconstruction' de la ligne qui aurait été reçue s'il y avait seulement le capteur TSL2561
        # afin d'employer la méthode de la classe associée pour l'insertion des données dans la base de données
        donnees_tsl = donnees[4:7]
        donnees_tsl.append(ms)
        self.tsl.inserer_bdd(' '.join(donnees_tsl))

    def afficher_console(self, ligne):
        # Version ~~'J'ai la flemme'~~ capitaliser sur le code préexistant afin de gagner en productivité
        donnees = ligne.split(" ")
        ms = donnees[7]

        donnees_car = donnees[0]  # Un seul élément : donnees_car est une str et n'est donc pas un tableau
        donnees_car += ' ' + ms  # Concaténation de str (à l'opposé des 'append' et 'join' dans la suite)
        self.car.afficher_console(donnees_car)

        donnes_dht = donnees[1:4]
        donnes_dht.append(ms)
        self.dht.afficher_console(' '.join(donnes_dht))

        donnees_tsl = donnees[4:7]
        donnees_tsl.append(ms)
        self.tsl.afficher_console(' '.join(donnees_tsl))

        print("==========================================================================")
