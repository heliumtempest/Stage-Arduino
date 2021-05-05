from Capteurs.CapteurInterface import CapteurInterface

class Capteur(CapteurInterface):

    def __init__(self):
        super(Capteur, self).__init__()
        self.affichage_console = "{u} t0+{ms} ms"
        #TODO faute de doc technique, je sais pas trop à quoi correspond la valeur mesurée (tension?)
        self.inserer_sql = "INSERT INTO \"Micro\"(\"Session\",\"Date\",\"Mesure\") " \
                           "VALUES('{s}','{ts}',{u});"

    def creer_table(self):
        # TODO modifier le nom de la colonne 'mesure' dès qu'on en saura un peu plus
        script = open("Capteurs/Micro/table_micro.sql")
        self.bdd.executer_requete(script.read())

    def ecrire_csv(self, ligne):
        #TODO faire ça mieux
        path = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\micro_{t0}.csv".format(t0=self.t0_str)
        csv = open(path, 'a')
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
        pass
