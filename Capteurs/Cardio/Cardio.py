import Capteurs.CapteurInterface as ci
from datetime import timedelta

class Capteur(ci.CapteurInterface):

    def __init__(self):
        super().__init__()

        self.affichage_console = "Pulsation cardiaque : {pc} bpm; T0+{ms}ms"  # bpm : battements par minute
        self.requete_insertion = "INSERT INTO Cardio(\"Date\", \"Session\", \"Pulsation\") VALUES('{d}', '{s}', {bpm});"

        #self.chemin_csv = "Capteurs/Cardio/csv/Cardio_" + self.t0_str + ".csv" #TODO  tester
        self.chemin_csv = "CSV/Cardio_" + self.t0_str + ".csv"
        # Création du fichier csv et écriture de l'en-tête
        en_tete = "Pulsation;Temps\n"
        csv = open(self.chemin_csv, 'a')
        csv.write(en_tete)
        csv.close()

    def ecrire_csv(self, ligne):
        csv = open(self.chemin_csv, 'a')
        csv.write(ligne.replace(' ', ';') + '\n')
        csv.close()

    def inserer_bdd(self, ligne):
        donnees = ligne.split(" ")
        timestamp = self.t0 + timedelta(milliseconds=int(donnees[1]))
        requete = self.requete_insertion.format(d=timestamp, s=self.bdd.nom_session, bpm=donnees[0])
        self.bdd.executer_requete(requete)

    def afficher_console(self, ligne):
        donnees = ligne.split(" ")
        affichage = self.affichage_console.format(pc=donnees[0], ms=donnees[1])
        print(affichage)

    def creer_table(self):
        script = open("Capteurs/Cardio/table_cardio.sql", 'r')
        self.bdd.executer_requete(script.read())
        script.close()