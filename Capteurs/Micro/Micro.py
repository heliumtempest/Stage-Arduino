from Capteurs.CapteurInterface import CapteurInterface

class Capteur(CapteurInterface):

    def __init__(self):
        super(Capteur, self).__init__()
        self.affichage_console = "Tension Micro:{u} t0+{ms} ms"
        self.inserer_sql = "INSERT INTO \"Micro\"(\"Session\",\"Date\",\"Tension\") " \
                           "VALUES('{s}','{ts}',{u});"

        #self.chemin_csv = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\micro_{t0}.csv".format(t0=self.t0_str)
        self.chemin_csv = "CSV\\micro_{t0}.csv".format(t0=self.t0_str) #TODO tester nouvel emplacement
        csv = open(self.chemin_csv, 'w')
        csv.write("Tension;Temps\n")
        csv.close()

    def creer_table(self):
        script = open("Capteurs/Micro/table_micro.sql")
        self.bdd.executer_requete(script.read())

    def ecrire_csv(self, ligne):
        csv = open(self.chemin_csv, 'a')
        csv.write(ligne.replace(' ', ';') + '\n')
        csv.close()

    def afficher_console(self, ligne):
        donnees = ligne.split(" ")
        affichage = self.affichage_console.format(u=donnees[0], ms=donnees[1])
        print(affichage)

    def inserer_bdd(self, ligne):
        donnees = ligne.split(" ")
        timestamp = self.ajouter_ms(self.t0, donnees[1])
        sql = self.inserer_sql.format(u=donnees[0], ts=timestamp, s=self.bdd.nom_session)
        self.bdd.executer_requete(sql)
