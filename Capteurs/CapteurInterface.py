import abc


class CapteurInterface(metaclass=abc.ABCMeta):

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
