"""
Nouvelle version du logiciel ViPPer 

Date: Août 2022

Améliorations: (Prévisions)
    - Nouvelle Interface Graphique
    - Nouvelle méthode de calcul
    - Amélioration de la rapidité d'exécution du programme
    
Ce script est dédié à la réalisation de la zone de dessin

"""

# Importation des modules
import sys
import qtall as qt

class _drawViPPer(qt.QWidget):
    def __init__(self):
        super(_drawViPPer, self).__init__()
        
        self._palette()

    def paintEvent(self, event):
        self.painter = qt.QPainter(self)
        pen = self.painter.setPen(qt.Qt.black)
        # Obtenir les coordonnées du centre de la zone
        center = self.rect().center()
        # Créer un objet de type Rectangle
        rect = qt.QRect(0,0,150,50)
        # Déplacer ce rectangle au milieu de la zone
        rect.moveCenter(center)
        # Dessiner le rectangle
        self.painter.drawRect(rect)
        # Ecrire du texte
        self.painter.drawText(rect, qt.Qt.AlignCenter, "Armature: 2 HA12")
        self.painter.end()
    
    def _palette(self):
        # set white background
        pal = self.palette()
        pal.setColor(qt.QPalette.Background, qt.Qt.white)
        self.setAutoFillBackground(True)
        self.setPalette(pal)
        
        
        