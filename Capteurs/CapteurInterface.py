import abc
from datetime import datetime
# TODO Possible de seulement prendre now() ?
import Commun.ConnexionPostgres as cpg
# TODO modification pour la co en static


class CapteurInterface(metaclass=abc.ABCMeta):

    # TODO modification pour la co en static
    # En espérant que la BDD soit héritée des classes filles
    # Sinon, on peut essayer une méthode GetBdd (pas abstraite cette fois)
    def __init__(self):
        # Il semble que c'est un échec
        self.bdd = cpg.ConnexionPostgres()
        self.t0 = datetime.now()
        self.t0_str = datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S')

    @abc.abstractmethod
    def afficher_console(self, ligne):
        pass

    @abc.abstractmethod
    def ecrire_csv(self, ligne):
        pass

    @abc.abstractmethod
    def inserer_bdd(self, ligne):
        pass

    @abc.abstractmethod
    def creer_table(self):
        pass
