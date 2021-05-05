from Capteurs.CapteurInterface import CapteurInterface


class Capteur(CapteurInterface):

    def __init__(self):
        super(Capteur, self).__init__()
        self.affichage = "X:{x} Y:{y} T0+{ms} ms"
        self.inserer_requete = "INSERT INTO \"Joystick\"(\"Session\",  \"X\", \"Y\", \"Date\")" \
                               "VALUES('{s}', {x}, {y}, '{ts}');"

    def creer_table(self):
        script = open("Capteurs/Joystick/table_joystick.sql", 'r')
        self.bdd.executer_requete(script.read())

    def ecrire_csv(self, ligne):
        # TODO faire un peu mieux
        path = "C:\\Users\\ghisl\\Desktop\\Stage\\dumpcsv\\joystick_{t0}.csv".format(t0=self.t0_str)
        csv = open(path, 'w')  # Le fichier est écrasé à chaque execution
        csv.write(ligne.replace(' ', ';') + '\n')
        csv.close()

    def inserer_bdd(self, ligne):
        donnees = ligne.split(" ")
        timestamp = self.ajouter_ms(self.t0, donnees[2])
        sql = self.inserer_requete.format(s=self.bdd.nom_session, x=donnees[0], y=donnees[1], ts=timestamp)
        self.bdd.executer_requete(sql)

    def afficher_console(self, ligne):
        donnees = ligne.split(" ")
        affichage = self.affichage.format(x=donnees[0], y=donnees[1], ms=donnees[2])
        print(affichage)
