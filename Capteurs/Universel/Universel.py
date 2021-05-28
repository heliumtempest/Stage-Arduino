from Capteurs.CapteurInterface import CapteurInterface as ci
from Capteurs.DHT22 import DHT22
from Capteurs.TSL2561 import TSL2561
from Capteurs.MPL3115 import MPL3115
from Capteurs.Cardio import Cardio
from Capteurs.Micro import Micro


class Capteur(ci):

    def __init__(self):
        # Constructeur de la classe mère (abtraite)
        super(Capteur, self).__init__()
        # Instanciation des classes de chacun des capteurs de manière individuelle
        self.dht = DHT22.Capteur()
        self.tsl = TSL2561.Capteur()
        self.mpl = MPL3115.Capteur()
        self.cardio = Cardio.Capteur()
        self.micro = Micro.Capteur()

        # self.csv_path = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\universel_{t0}.csv".format(t0=self.t0_str)
        self.csv_path = "CSV\\universel_{t0}.csv".format(t0=self.t0_str) #TODO tester le nouvel emplacement
        csv_header = "Humidite;Temperature_1;Indice;Lux;LumIR;LumSE;Pression;Temperature_2;Pulsation;Micro\n"
        csv = open(self.csv_path, 'w')
        csv.write(csv_header)
        csv.close()


    def creer_table(self):
        # Chaque capteur crée la table qui lui est propre à l'aide de l'instace de sa classe
        self.dht.creer_table()
        self.tsl.creer_table()
        self.mpl.creer_table()
        self.cardio.creer_table()
        self.micro.creer_table()

    # Remarque la ligne envoyée par le arduino
    # humidité, température, indice de chaleur, lux, lum. IR, lum. spectre entier, pression, temperature, bpm, son, millisecondes
    # Si le capteur n'est pas présent, les valeurs qu'il aurait dû mesurée sont remplacée par le caractère '\'

    def inserer_bdd(self, ligne):
        donnees = ligne.split(" ")
        ms = donnees[11]  # millisecondes écoulées depuis le lancement du programme arduino

        # Remarque : la borne supérieure (3) n'est pas incluse,
        # la liste contient donc les éléments d'indice 0, 1 et 2 mais pas d'indice 3
        champs_dht = donnees[0:3]
        champs_dht.append(ms)
        ligne_dht = " ".join(champs_dht)
        if(champs_dht[0] != '/'):  # Vérification que les données du capteur existent
            self.dht.inserer_bdd(ligne_dht)

        champs_tsl = donnees[3:6]
        champs_tsl.append(ms)
        ligne_tsl = " ".join(champs_tsl)
        if(champs_tsl[0] != '/'):
            self.tsl.inserer_bdd(ligne_tsl)

        champs_mpl = donnees[6:9]
        champs_mpl.append(ms)
        ligne_mpl = " ".join(champs_mpl)
        if(champs_mpl[0] != '/'):
            self.mpl.inserer_bdd(ligne_mpl)

        # Extraction d'un seul élément d'un tableau de chaînes de caractères
        # C'est donc une chaîne de caractère et non pas un tableau contrairement aux cas ci-dessus
        ligne_cardio = donnees[9]
        if(ligne_cardio != '/'):
            ligne_cardio += " " + ms
            self.cardio.inserer_bdd(ligne_cardio)

        ligne_micro = donnees[10]
        if(ligne_micro != '/'):
            ligne_micro += " " + ms
            self.micro.inserer_bdd(ligne_micro)

        print("========================================================")

    def ecrire_csv(self, ligne):
        ligne = ligne.replace(' ', ';')
        ligne = ligne.replace('/', '')
        csv = open(self.csv_path, 'a')
        csv.write(ligne + '\n')
        csv.close()


    def afficher_console(self, ligne):
        donnees = ligne.split(" ")
        ms = donnees[11]  # millisecondes écoulées depuis le lancement du programme arduino

        # Remarque : la borne supérieure (3) n'est pas incluse,
        # la liste contient donc les éléments d'indice 0, 1 et 2 mais pas d'indice 3
        champs_dht = donnees[0:3]
        champs_dht.append(ms)
        ligne_dht = " ".join(champs_dht)
        if (champs_dht[0] != '/'):  # Vérification que les données du capteur existent
            self.dht.afficher_console(ligne_dht)

        champs_tsl = donnees[3:6]
        champs_tsl.append(ms)
        ligne_tsl = " ".join(champs_tsl)
        if (champs_tsl[0] != '/'):
            self.tsl.afficher_console(ligne_tsl)

        champs_mpl = donnees[6:9]
        champs_mpl.append(ms)
        ligne_mpl = " ".join(champs_mpl)
        if (champs_mpl[0] != '/'):
            self.mpl.afficher_console(ligne_mpl)

        # Extraction d'un seul élément d'un tableau de chaînes de caractères
        # C'est donc une chaîne de caractère et non pas un tableau contrairement aux cas ci-dessus
        ligne_cardio = donnees[9]
        if (ligne_cardio != '/'):
            ligne_cardio += " " + ms
            self.cardio.afficher_console(ligne_cardio)

        ligne_micro = donnees[10]
        if (ligne_micro != '/'):
            ligne_micro += " " + ms
            self.micro.afficher_console(ligne_micro)