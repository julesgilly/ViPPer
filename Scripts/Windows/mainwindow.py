"""
Nouvelle version du logiciel ViPPer 

Date: Août 2022

Améliorations: (Prévisions)
    - Nouvelle Interface Graphique
    - Nouvelle méthode de calcul
    - Amélioration de la rapidité d'exécution du programme
    
Ce script est dédié à la réalisation de la fenêtre principale de l'interface grphique du logiciel
On y trouvera:
    - Une menu bar contenant des onglets pour chaque étape de remplissage pour l'utilisateur
    - Une zone de dessin qui s'actualisera au fur et à mesure du remplissage des données
    
La zone de dessin devra:
    - Afficher un schéma du VPP, du type de sol, des charges mise en jeu à l'échelle
    - Afficher le nom de l'ingénieur, la date, le nom du projet, le nom de la coupe et un logo (logiciel ou entreprise)
    - Etre imprimable et enregistrable

"""

# Importation des modules
import sys
import os
import os.path
import qtall as qt
import Drawings as dr

class _MainWindow(qt.QMainWindow):
    def setupUi(self, MainWindow):
        # qt.QMainWindow.__init__(self, *args)
        # Création de la fenêtre principale
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        # Créer un centralwidget sur la fenêtre princiaple
        self.centralwidget = qt.QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # Fixer la taille de la MainWindow
        self._defineWindowSize(MainWindow)
        
        # icone sur la fenêtre principale
        #self.setWindowIcon( 'chemin vers l icone' )
        
        # filename pour le projet et actualiser la titlebar
        self.filename = ''
        self.updateTitlebar(MainWindow)
        
        # Créer menus et toolbars
        self._defineMenus(MainWindow)
        
        # Définir la font
        self._defineFont(MainWindow)

        # Créer la zone de dessin
        self.createZone(MainWindow)
        
        # Nommer les différents objets
        self.retranslateUi(MainWindow)
        
        MainWindow.setCentralWidget(self.centralwidget)
        qt.QMetaObject.connectSlotsByName(MainWindow)
    
    def _defineFont(self, MainWindow):
        """Définir les polices d'écriture, la taille de la police et l'associer à la fenetre"""
        font = qt.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        MainWindow.setFont(font)
        
    def _defineMenus(self, MainWindow):
        """Initialise the menus and toolbar."""
        # Création de la menu bar
        self.menubar = qt.QMenuBar(MainWindow)
        self.menubar.setGeometry(qt.QRect(0, 0, self.width, 24))
        self.menubar.setObjectName("menubar")
        self.menuFichier = qt.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = qt.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFichier.menuAction())
       
        self.exitAction = qt.QAction(MainWindow)        
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(MainWindow.close)
        self.menuFichier.addAction(self.exitAction)
    
    def _defineWindowSize(self, MainWindow):
        """ Fixer la taille initiale de la fenetre et la Size policy"""
        self.width = 1700
        self.height = 840
        MainWindow.resize(self.width, self.height)
        
        # Définir les régles sur les dimensions de la fenêtre
        sizePolicy = qt.QSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
    
    def createZone(self, MainWindow):
        # Créer des layout dans le widget pour y placer la zone de dessin
        self.gridLayout = qt.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = qt.QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        # Appeler et Ajouter le widget résultant de la class de Dessin dans le layout dans la fenêtre principale
        self.verticalLayout.addWidget(dr._drawViPPer())
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        
    def updateTitlebar(self, MainWindow):
        """Afficher le nom du fichier dans la titlebar"""
        if self.filename == '':
            MainWindow.setWindowTitle(('Untitled - ViPPer: Logiciel de dimensionnement des voiles par passes alternées'))
        else:
            MainWindow.setWindowTitle(
                ("%s - ViPPer: Logiciel de dimensionnement des voiles par passes alternées") % os.path.basename(self.filename))
          
    def retranslateUi(self, MainWindow):
        _translate = qt.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Logiciel de dimensionnement des voiles par passes alternées"))
        
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.exitAction.setText(_translate("MainWindow", "Quitter"))


