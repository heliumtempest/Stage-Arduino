import abc
from datetime import datetime, timedelta
import Commun.ConnexionPostgres as cpg


class CapteurInterface(metaclass=abc.ABCMeta):
    """Classe abstraite qui contient des méthodes à implémenter pour tous les capteurs ainsi que certains attributs."""

    def __init__(self):
        self.bdd = cpg.ConnexionPostgres()  # Connexion vers la base de données
        self.t0 = datetime.now()  # Timestamp qui correspond au moment de l'instanciation de la classe (ou de ses classes filles)
        self.t0_str = datetime.strftime(self.t0, '%Y-%m-%d_%H-%M-%S')  # Conversion du timestamp en chaîne de caractère
        # Remarque : pour que ces attributs soient hérités dans les classes filles, leur contructeur (__init__) doit
        # comporter l'instruction : super().__init__()

    @abc.abstractmethod
    def afficher_console(self, ligne):
        """Affiche pour la ligne lue en provenence du capteur le message à faire apparaître dans la console."""
        pass

    @abc.abstractmethod
    def ecrire_csv(self, ligne):
        """Écrit une ligne dans le fichier csv qui correspond à la ligne lue depuis le capteur."""
        pass

    @abc.abstractmethod
    def inserer_bdd(self, ligne):
        """Ajoute pour chaque ligne lue en provenence du capteur l'enregestriment associé dans la base de données."""
        pass

    @abc.abstractmethod
    def creer_table(self):
        """Execute le script qui correspond à la création de la table contenant les mesures du capteurs dans la base de
        données."""
        pass

    def ajouter_ms(self, timestamp, millisecondes):
        """Ajoute des millisecondes à un timestamp et retourne le timestamp correspondant"""
        # Les millisecondes sont converties en un entier, 'millisecondes' peut donc être une chaîne de caractère
        return timestamp + timedelta(milliseconds=int(millisecondes))
