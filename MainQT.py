# TODO Installation de QT nécessaire, faire un try/except pour importation
# pip install pyside6
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import * # Il a changé de place... (les QActions)
import sys
import Commun.Port
import Forms.ParamBDD


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.port = Commun.Port.Port()

        self.setWindowTitle("Fenêtre principale")

        # Déclaration des différents composants
        #TODO on n'est peut-etre pas obligé de tout mettre en attribut
        self.portsCombobox = QComboBox()
        self.portsCombobox.addItems(self.port.ports_dispo())
        self.actualiserButton = QPushButton("Actualiser")
        self.connexionButton = QPushButton("Connexion")
        self.affichageTextedit = QTextEdit()
        # Les actions pour le menu
        action_ouvrirParamBDD = QAction("Base de données", self)
        action_ouvrirParamBDD.triggered.connect(self.ouvrir_paramBB) # J'ai bien galéré pour trouvé comment faire
        # Le menu
        barreMenu = QMenuBar()
        menuParametre = barreMenu.addMenu("Paramètres")
        menuBDD = menuParametre.addAction(action_ouvrirParamBDD)
        #menuParametre.addAction("Capteur") #Utilité
        self.setMenuBar(barreMenu)

        # On essaie de faire ces ptn d'action

        # Assigner à la classe port la 'textEdit' afin de pouvoir écrire dessus
        self.port.textBoxQT = self.affichageTextedit

        self.affichageTextedit.setReadOnly(True)  # Rend le contenu non éditable

        # Mise en page des composants (version QWidget)
        # addWidget (self, QWidget, row, column, rowSpan, columnSpan, Qt.Alignment alignment = 0)
        # self.layout = QGridLayout(self)
        # self.layout.addWidget(self.portsCombobox, 0, 0, 1, 2)  # 1ère ligne sur 2 colonnes
        # self.layout.addWidget(self.actualiserButton, 1, 0)  # 2ème ligne, 1ère colonne
        # self.layout.addWidget(self.connexionButton, 1, 1)  # 2ème ligne, 2ème colonne
        # self.layout.addWidget(self.affichageTextedit, 2, 0, -1, -1) # Tout l'espace restant disponible

        # Mise en page des composants (version QMainWindow)
        layout = QGridLayout()
        mainWidget = QWidget()
        layout.addWidget(self.portsCombobox, 0, 0, 1, 2)
        layout.addWidget(self.actualiserButton, 1, 0)  # 2ème ligne, 1ère colonne
        layout.addWidget(self.connexionButton, 1, 1)  # 2ème ligne, 2ème colonne
        layout.addWidget(self.affichageTextedit, 2, 0, -1, -1)  # Tout l'espace restant disponible
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        # Assignation des fonctions des boutons #TODO mieux formuler
        self.actualiserButton.clicked.connect(self.actualisation)
        self.connexionButton.clicked.connect(self.connexion)


    @QtCore.Slot()
    def actualisation(self):
        self.portsCombobox.clear()
        self.portsCombobox.addItems(self.port.ports_dispo())

    @QtCore.Slot()
    def connexion(self):
        nom_port = self.portsCombobox.currentText()
        self.port.assigner_port(nom_port)
        self.port.bdd = self.fenetre.pg # TODO c'est pas très clair sans contexte
        self.port.lire_port()

    @QtCore.Slot()
    def ouvrir_paramBB(self):
        # TODO passer 'self' dans le constructeur de la fenêtre (ça peut clairement être amélioré)
        self.fenetre = Forms.ParamBDD.ParamBDD()
        self.fenetre.show()


if __name__ == "__main__":
    app = QApplication([])
    mw = MainWindow()
    mw.resize(200, 200)
    mw.show()

    sys.exit(app.exec_())

# Créer une boîte de dialogue pour afficher un message :
# test = QMessageBox()
# test.setText("Port assigné : " + self.port.port.name)
# test.exec_()
