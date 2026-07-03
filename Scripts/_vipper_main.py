# ViPPer - Logiciel de dimensionnement des voiles par passes alternées
# Copyright (C) : Jules GILLY <julesgilly@gmail.com>
###############################################################################

""" Main script for ViPPer """

import sys
import os
import os.path

import qtall as qt
import Windows
import Drawings

if sys.version_info[0] < 3:
    raise RuntimeError('ViPPer only supports Python 3')

# Copyrights
copyr='''ViPPer %s
Copyright (C) Jules GILLY 2021-2022 <julesgilly@gmail.com>
'''
splashcopyr='''<b><font color="purple">ViPPer %s<br></font></b>
Copyright (C) Jules GILLY 2021-2022 
'''

if __name__ == '__main__':
    print('run')
    app = qt.QApplication(sys.argv)
    MainWindow = qt.QMainWindow()
    ui = Windows._MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())