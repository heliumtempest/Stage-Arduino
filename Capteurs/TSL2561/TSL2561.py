from datetime import datetime, timedelta

class Capteur():

    bdd = None
    t0 = datetime.now()

    def afficher_console(self,ligne):
        print(ligne)

    def inserer_bdd(self, ligne):
        return

    def ecrire_csv(self, ligne):
        return