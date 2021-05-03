import Capteurs.CapteurInterface as ci
import Capteurs.TSL2561.TSL2561 as tsl
import Capteurs.DHT22.DHT22 as dht
import Capteurs.Cardio.Cardio as car


class Capteur(ci.CapteurInterface):

    def __init__(self):
        super(Capteur, self).__init__()
        self.dht = dht.Capteur()
        self.tsl = tsl.Capteur()
        self.car = car.Capteur()


    def creer_table(self):
        self.dht.creer_table()
        self.tsl.creer_table()
        self.car.creer_table()

    def ecrire_csv(self, ligne):
        # TODO un seul csv ou plusieurs...
        # donnees = ligne.split(" ")
        #
        # donnes_car = donnees[0]
        # donnes_car.append(donnees[7])
        # self.car.ecrire_csv(';'.join(donnes_car))

        # TODO 'version rapide' à faire en un peu plus rigoureux (il n'y a pas de header entre autre)
        path = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\trio_{t0}.csv".format(t0=self.t0_str)
        csv = open(path, 'a')
        csv.write(ligne.replace(' ', ';') + "\n")
        csv.close()


    def inserer_bdd(self, ligne):

        donnees = ligne.split(" ")
        ms = donnees[7]

        donnes_car = donnees[0]
        donnes_car += ' ' + ms
        self.car.inserer_bdd(donnes_car)

        donnes_dht = donnees[1:4]
        donnes_dht.append(ms)
        self.dht.inserer_bdd(' '.join(donnes_dht))

        donnees_tsl = donnees[4:7]
        donnees_tsl.append(ms)
        self.tsl.inserer_bdd(' '.join(donnees_tsl))

    def afficher_console(self, ligne):
        # Version ~~'J'ai la flemme'~~ capitaliser sur le code préexistant afin de gagner en productivité
        donnees = ligne.split(" ")
        ms = donnees[7]

        donnees_car = donnees[0]  # Un seul élément : donnees_car est une str
        donnees_car += ' ' + ms  # Concaténation de str (à l'opposé des 'append' dans la suite)
        self.car.afficher_console(donnees_car)

        donnes_dht = donnees[1:4]
        donnes_dht.append(ms)
        self.dht.afficher_console(' '.join(donnes_dht))

        donnees_tsl = donnees[4:7]
        donnees_tsl.append(ms)
        self.tsl.afficher_console(' '.join(donnees_tsl))

        print("==========================================================================")