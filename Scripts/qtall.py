# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################

"""A convenience module to import used Qt symbols from."""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtPrintSupport import *
from PyQt5.uic import loadUi

try:
    from PyQt5 import sip
except ImportError:
    import sip
