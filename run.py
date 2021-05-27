"""
pip to do :
pip install QtAwesome
pip install pygmsh
pip install gmsh


"""

import sys
import os
from PyQt5.QtWidgets import *
#QMainWindow,QApplication,QRadioButton,QWidget,QPushButton,QAction,QLineEdit,QGridLayout,QGroupBox,QMessageBox,QHBoxLayout,QComboBox,QVBoxLayout,QLabel,QStatusBar,QCheckBox,QSlider,QFileDialog,QTabWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome as qta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pygmsh
#from Test23 import *

#https://www.mfitzp.com/tutorials/layouts/

class Canvas(FigureCanvas):
    def __init__(self,parent):
        fig, self.ax = plt.subplots(figsize=(5,4),dpi=200)
        super().__init__(fig)
        self.setParent(parent)
        t = np.arange(0,2,0.1)
        s = np.sin(t)
        self.ax.plot(t,s)
        self.ax.set(xlabel="time",ylabel="sin",title="test")
        self.ax.grid()

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class IconLabel(QWidget):

    IconSize = QSize(16, 16)
    HorizontalSpacing = 1

    def __init__(self, qta_id, text, final_stretch=True):
        super(QWidget, self).__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(qta.icon(qta_id).pixmap(self.IconSize))

        layout.addWidget(icon)
        layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(QLabel(text))

        if final_stretch:
            layout.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


        self.setMinimumSize(QSize(1200, 1000)) #Window size width and height
        self.setWindowTitle("C2A - Chaine de Calcul Aerodynamique")
        self.setWindowIcon(QIcon("gears.png"))

        # Create new action
        newAction = QAction(QIcon('new.png'), '&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New document')
        newAction.triggered.connect(self.newCall)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open document')
        openAction.triggered.connect(self.getFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)


        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        menuBar.addMenu('Parameters')
        menuBar.addMenu('Tools')
        menuBar.addMenu('Help')

        # Add Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Current Folder Location :" + os.getcwd())

        # Creation ComboBox
        #solver
        self.cb1 = QComboBox()
        self.cb1.addItems(["JST","LAX-FRIEDRICH","CUSP","ROE","AUSM","HLLC","TURKEL_PREC","MSW"])
        self.cb1.currentIndexChanged.connect(self.selectionchange)
        self.cb2 = QComboBox()
        self.cb2.addItems(["RUNGE-KUTTA_EXPLICIT","EULER_IMPLICIT","EULER_EXPLICIT"])
        self.cb3 = QComboBox()
        self.cb3.addItems(["EULER", "NAVIER_STOKES","WAVE_EQUATION", "HEAT_EQUATION", "FEM_ELASTICITY","POISSON_EQUATION"])

        # Creation checkbox
        self.checkbox1 = QCheckBox("Plot", self)
        self.checkbox2 = QCheckBox("Reconstruction MUSCL", self)
        self.checkbox3 = QCheckBox("Acceleration Multigrid", self)

        # Creation d'un slider
        self.sl1 = QSlider(Qt.Horizontal)
        self.sl1.setFocusPolicy(Qt.StrongFocus)
        self.sl1.setTickPosition(QSlider.TicksBothSides)
        self.sl1.setTickInterval(10)
        self.sl1.setSingleStep(1)
        self.sl1.setMinimum(0)
        self.sl1.setMaximum(10)
        self.sl1.valueChanged.connect(self.value_changed)

        # Creation des labels
        #maillage
        self.l11 = QLabel('Charger un maillage : ')

        #solver
        self.l0 = QLabel('Solver :')
        self.l1 = QLabel('Choix du schéma spacial :', self)
        self.l2 = QLabel('Choix du schéma temporel :', self)
        self.l3 = QLabel('Entrer un CFL :', self)
        self.l4 = QLabel('CFL Choisi :' + str(self.sl1.value()), self)
        self.l5 = QLabel('Mach Number :')
        self.l6 = QLabel('FREESTREAM_PRESSURE :')
        self.l7 = QLabel('FREESTREAM_Temperature :')

        # Creation des boutons
        #maillage
        self.Load_mesh = QPushButton("Charger un maillage .su2")
        self.Load_mesh.clicked.connect(self.getFile)
        self.Launch1 = QPushButton("Lancer GMSH")
        self.Launch1.clicked.connect(self.Click_gmsh)
        #solver
        self.b1 = QPushButton("Lancer la simu")
        self.b1.clicked.connect(self.Click1)
        self.Load_cfg = QPushButton("Charger un config .cfg")
        self.Load_cfg.clicked.connect(self.getFile)
        self.Launch2 = QPushButton("Lancer SU2")
        self.Launch2.clicked.connect(self.Click_su2)
        #post
        self.Launch3 = QPushButton("Lancer PARAVIEW")
        self.Launch3.clicked.connect(self.Click_paraview)

        # Creation textbox
        #maillage
        self.t11 = QLineEdit()

        #solver
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.t4 = QLineEdit()

        #Creation Groupbox
        self.groupbox1 = QGroupBox("Maillage :")
        self.groupbox2 = QGroupBox("Paramètre de simulation numérique :")
        self.groupbox3 = QGroupBox("Post-traitement :")

        #Layout horizontal
        hbox = QHBoxLayout()
        self.setLayout(hbox)

        ######### STRUCTURE ############
        ### MAILLAGE
        vbox1 = QVBoxLayout()
        self.groupbox1.setLayout(vbox1)

        self.radiobutton = QRadioButton("Structuré")
        vbox1.addWidget(self.radiobutton)
        self.radiobutton = QRadioButton("Non Structuré")
        vbox1.addWidget(self.radiobutton)
        self.radiobutton = QRadioButton("Hybride")
        vbox1.addWidget(self.radiobutton)
        self.radiobutton = QRadioButton("Chimère")
        vbox1.addWidget(self.radiobutton)
        vbox1.addStretch(1)
        #vbox1.addWidget(self.l11)
        vbox1.addWidget(IconLabel("fa.angle-double-right", "Charger un maillage .su2 :"))
        vbox1.addWidget(self.t11)
        vbox1.addWidget(self.Load_mesh)
        vbox1.addWidget(self.Launch1)

        ### SOLVER
        vbox2 = QVBoxLayout()
        self.groupbox2.setLayout(vbox2)

        vbox2.addWidget(IconLabel("fa.wrench", "Choix du solver :"))
        #vbox2.addWidget(self.l0)
        vbox2.addWidget(self.cb3)
        vbox2.addWidget(self.l1)
        vbox2.addWidget(self.cb1)
        vbox2.addStretch()
        vbox2.addWidget(self.l2)
        vbox2.addWidget(self.cb2)
        vbox2.addStretch()
        vbox2.addWidget(self.l3)
        vbox2.addWidget(self.t1)
        vbox2.addWidget(self.b1)
        vbox2.addStretch()
        vbox2.addWidget(self.l4)
        vbox2.addWidget(self.sl1)
        vbox2.addWidget(self.l5)
        vbox2.addWidget(self.t2)
        vbox2.addWidget(self.l6)
        vbox2.addWidget(self.t3)
        vbox2.addWidget(self.l7)
        vbox2.addWidget(self.t4)
        vbox2.addWidget(self.checkbox1)
        vbox2.addWidget(self.checkbox2)
        vbox2.addWidget(self.checkbox3)
        vbox2.addWidget(self.Launch2)

        ### MAILLAGE
        vbox3 = QVBoxLayout()
        self.groupbox3.setLayout(vbox3)

        self.radiobutton = QRadioButton("Structuré")
        vbox3.addWidget(self.radiobutton)
        self.radiobutton = QRadioButton("Non Structuré")
        vbox3.addWidget(self.radiobutton)
        vbox3.addStretch(1)
        vbox3.addWidget(self.Launch3)

        hbox.addWidget(self.groupbox1)
        hbox.addWidget(self.groupbox2)
        hbox.addWidget(self.groupbox3)
        hbox.addWidget(Canvas(self))


        widget = QWidget()
        widget.setLayout(hbox)
        self.setCentralWidget(widget)

    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function
        """
        self.filename = QFileDialog.getOpenFileName()[0] #argument : filter="csv (*.csv)"
        print("File :", self.filename)
        self.statusBar.showMessage("Maillage chargé : " + self.filename)
        self.t11.setText(self.filename)

    def value_changed(self):
        self.l4.setText('CFL Choisi :' + str(self.sl1.value()))


    def selectionchange(self, i):
        print("Items in the list are :")

        for count in range(self.cb1.count()):
            print(self.cb1.itemText(count))
        print("Current index", i, "selection changed ", self.cb1.currentText())

    def Click1(self):
        check = self.checkbox1.isChecked()
        print(check)
        # inputCFL = float(self.t1.text())
        inputCFL = self.sl1.value()
        print(self.sl1.value())
        print("Run Simulation")
        self.statusBar.showMessage('Run Simulation')
        simu(m=201, CFL=inputCFL, plot=check)  # CFL = 0.8
        self.statusBar.showMessage('End Simulation')

    def Click_gmsh(self):
        self.statusBar.showMessage('Lancement de GMSH')
        os.system("C://Users//Gameiro//Documents//CFD//gmsh-4.8.4-Windows64//gmsh.exe")

    def Click_su2(self):
        #On doit se deplacer pour se mettre dans le dossier du fichier ou alors on peut mettre dans le fichier config le chemin absolu du fichier maillage
        #on triche :
        os.chdir("C://Users//Gameiro//Documents//CFD//SU2-master//QuickStart")
        print(os.getcwd())
        self.statusBar.showMessage('Lancement de SU2')
        #recupère le nom fichier config
        config_name = self.t11.text()
        os.system("SU2_CFD "+ config_name) #inv_NACA0012.cfg

    def Click_paraview(self):
        self.statusBar.showMessage('Lancement de PARAVIEW')
        file = 'C:\\Program Files\\ParaView 5.9.1-Windows-Python3.8-msvc2017-64bit\\bin\\paraview.exe'
        os.system('"' + file + '"')

    def openCall(self):
        print('Open')

    def newCall(self):
        print('New')

    def exitCall(self):
        print('Exit app')
        sys.exit(app.exec_())

def main():
    app = QApplication(sys.argv)
    #ex = combodemo()
    #ex.show()
    mainWin = MainWindow()
    #['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyle('Fusion')
    mainWin.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


