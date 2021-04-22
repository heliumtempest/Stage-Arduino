from PySide6 import QtCore
from PySide6.QtWidgets import *
import sys
import Commun.ConnexionPostgres

class ParamBDD(QWidget):

    # def __init__(self, parent=None):
    #     super(ParamBDD, self).__init__(parent)
    def __init__(self):
        super().__init__()

        self.pg = Commun.ConnexionPostgres.ConnexionPostgres()

        layout = QFormLayout()

        #TODO enlever debug
        # self.setVisible(True)
        # print(self.isVisible())
        # print("Coucou du constructeur")

        # Définition des labels
        serveurLabel = QLabel("Adresse du serveur")
        utilisateurLabel = QLabel("Utilisateur")
        mdpLabel = QLabel("Mot de passe")
        bddLabel = QLabel("Base de données")
        # Définitions des zones éditables
        self.serveurLineEdit = QLineEdit()
        self.utilisateurLineEdit= QLineEdit()
        self.mdpLineEdit= QLineEdit()
        self.bddLineEdit = QLineEdit()
        # ... et avec remplies avec des valeurs par défaut
        self.serveurLineEdit.setText("127.0.0.1")
        self.utilisateurLineEdit.setText("postgres")
        self.mdpLineEdit.setText("admin")
        self.bddLineEdit.setText("arduino")
        # Définition des boutons
        validerButton = QPushButton("Valider")
        annulerButton = QPushButton("Annuler")
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(annulerButton)
        buttonLayout.addWidget(validerButton)
        # Mise en page
        layout.addRow(serveurLabel, self.serveurLineEdit)
        layout.addRow(utilisateurLabel, self.utilisateurLineEdit)
        layout.addRow(mdpLabel, self.mdpLineEdit)
        layout.addRow(bddLabel, self.bddLineEdit)
        layout.addRow(buttonLayout)

        self.setLayout(layout)
        self.setWindowTitle("Paramètres base de données")

        annulerButton.clicked.connect(self.annuler)
        validerButton.clicked.connect(self.valider)

    @QtCore.Slot()
    def annuler(self):
        self.close()

    def valider(self):
        self.pg.serveur = self.serveurLineEdit.text()
        self.pg.utilisateur =self.utilisateurLineEdit.text()
        self.pg.mot_de_passe = self.mdpLineEdit.text()
        self.pg.base_de_donnees = self.bddLineEdit.text()

        # Petit contôle
        self.pg.afficher_info()

        # Les informations sont saisies, la fenêtres peut être fermée
        self.close()


# test
# if __name__ == "__main__":
#     app = QApplication([])
#     mw = ParamBDD()
#     mw.resize(350, 200)
#     mw.show()
#
#     sys.exit(app.exec_())