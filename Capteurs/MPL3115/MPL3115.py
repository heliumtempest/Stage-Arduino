from Capteurs.CapteurInterface import CapteurInterface as ci


class Capteur(ci):

    def __init__(self):
        super(Capteur, self).__init__()

        self.affichage = "Pression:{Pa}, Altitude:{h}, Température:{T}, T0+{ms} ms"
        self.inserer = "INSERT INTO mpl3115(\"Session\", \"DateMesure\", \"Pression\", \"Altitude\", \"Temperature\") " \
                       "VALUES('{s}', '{ts}', {Pa}, {h}, {T});"

        self.chemin_csv = "CSV\\mpl_" + self.t0_str + ".csv"
        #TODO tester le nouvel emplacement du csv
        csv = open(self.chemin_csv, 'w')
        csv.write("Pression;Altitude;Temperature;Temps_ecoule\n")
        csv.close()


    def ecrire_csv(self, ligne):
        csv = open(self.chemin_csv, 'a')
        csv.write(ligne.replace(' ', ';') + "\n")
        csv.close()


    def inserer_bdd(self, ligne):
        donnees = ligne.split(" ")
        timestamp = self.ajouter_ms(self.t0, donnees[3])
        sql = self.inserer.format(s=self.bdd.nom_session, ts=timestamp, Pa=donnees[0], h=donnees[1], T=donnees[2])
        self.bdd.executer_requete(sql)

    def afficher_console(self, ligne):
        donnees = ligne.split(" ")
        affichage = self.affichage.format(Pa=donnees[0], h=donnees[1], T=donnees[2], ms=donnees[3])
        print(affichage)

    def creer_table(self):
        script = open("Capteurs/MPL3115/table_mpl3115.sql", 'r')
        self.bdd.executer_requete(script.read())
        script.close()
