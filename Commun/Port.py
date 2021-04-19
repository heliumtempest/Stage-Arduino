import serial.tools.list_ports
# Je crois qu'il faut installer 'pyserial' avant
import time
import importlib

# TODO le code est pas très "propre"
# TODO faire des try/except un peu partout
class Port:
    baud = 9600  # A specifier si besoin
    port = None
    bdd = None #TODO voir comment faire ça plus efficacement

    def selectionner_port(self):
        liste_ports = serial.tools.list_ports.comports(include_links=False)
        nombre_ports = len(liste_ports)
        if(nombre_ports == 0):
            print("Aucun port n'a été trouvé")
            exit()
        elif(nombre_ports == 1):
            self.port = liste_ports[0]
            print("Un port trouvé : ", self.port.name)
            #self.choix_port = 0

        else: # Plus de 1 port
            print("Port disponibles :")
            num_port = 0
            for port in liste_ports:
                print("Port n°", num_port, ":", port.name)
            choix_port = input("Choix du numéro de port à sélectionner : ")
            self.port = liste_ports[choix_port]

    def lire_port(self):
        #port = self.selectionner_port()
        print("Connexion au port : ", self.port)

        if self.port is None:
            print("Fermeture de l'appli")
            exit()

        arduino = serial.Serial(self.port.device, baudrate=self.baud)
        print('Connexion à ' + arduino.name + ' à une vitesse en baud de ' + str(self.baud))

        # Réinitialisation
        arduino.setDTR(False)
        time.sleep(0.1)
        arduino.setDTR(True)

        # Vidage du Buffer
        arduino.flushInput()

        #Lecture de la 1ère ligne reçue
        ligne_1 = arduino.readline().decode("utf-8")
        id_programme = ligne_1[:-2]  # Retrait du '\n' de fin de ligne
        # Importation du module correspondant
        # Attention à bien vérifier l'exactitude des noms
        module = "Capteurs." + id_programme + "." + id_programme
        cl_cpt = importlib.import_module(module)
        cpt = cl_cpt.Capteur()
        if(self.bdd != None):
            cpt.bdd = self.bdd
        else:
            print("Erreur, la connewion transmise au port n'est pas valide")
            exit()

        # Lecture en continu du reste des données
        try:
            while True:
                ligne = arduino.readline().decode("utf-8")
                ligne = ligne[:-2]  # Retrait du '\n' de fin de ligne
                if ligne != "":
                    # Opérations liées au capteur
                    cpt.afficher_console(ligne)
                    cpt.inserer_bdd(ligne)
                    cpt.ecrire_csv(ligne)
        except:
            print("Lecture interrompue")
            raise


# Zone pour test
# test = Port()
# test.selectionner_port()
# test.lire_port()