"""
Author : GAMEIRO Nicolas

Description :
Application in pyQt5 to run SU2 Code, gmsh and paraview easily for numerical simulation

Date Creation : 20/05/2021
Last Update : 27/05/2021
"""
import glob
import sys
import os
import subprocess
import shlex
import re
from PyQt5.QtWidgets import *
#QMainWindow,QApplication,QRadioButton,QWidget,QPushButton,QAction,QLineEdit,QGridLayout,QGroupBox,QMessageBox,QHBoxLayout,QComboBox,QVBoxLayout,QLabel,QStatusBar,QCheckBox,QSlider,QFileDialog,QTabWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import qtawesome as qta
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 12
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#import pygmsh

#Script Appli
from Reader import *

#https://www.mfitzp.com/tutorials/layouts/

class Canvas(FigureCanvas):
    def __init__(self,parent):
        fig, self.ax = plt.subplots(figsize=(5,4),dpi=200)
        super().__init__(fig)
        self.setParent(parent)
        '''
        i = 0
        while model.item(i):
            if model.item(i).checkState():
                i += 1
        '''
        filename = "Test/history.csv" #model.item(i).text() "Test/history.csv"
        res = Read_res(filename)
        self.ax.plot(res[0],res[1],label="ro")
        self.ax.plot(res[0], res[2],label="rou")
        self.ax.plot(res[0], res[3],label="rov")
        self.ax.set(xlabel="iteration",ylabel="Residu",title="Convergence")
        self.ax.legend()
        self.ax.grid()

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
        self.initUI()
        self.Tab_Maillage()
        self.Tab_Solver()
        self.Tab_Post()
        self.body()

    def initUI(self):
        ### Paramètres de définition de la fenetre principale
        self.setMinimumSize(QSize(200, 400)) #Window size width and height
        width, height = 600, 1000
        self.setFixedWidth(width) # setting  the fixed width of window
        self.setFixedHeight(height)  # setting  the fixed width of window
        self.setWindowTitle("C2A - Chaine de Calcul Aerodynamique")
        self.setWindowIcon(QIcon("gears.png"))

    def Tab_Maillage(self):
        return

    def Tab_Solver(self):
        self.cb1 = QComboBox()
        self.cb1.addItems(["JST", "LAX-FRIEDRICH", "CUSP", "ROE", "AUSM", "HLLC", "TURKEL_PREC", "MSW"])
        self.cb1.currentIndexChanged.connect(self.selectionchange)
        self.cb2 = QComboBox()
        self.cb2.addItems(["RUNGE-KUTTA_EXPLICIT", "EULER_IMPLICIT", "EULER_EXPLICIT"])
        self.cb3 = QComboBox()
        self.cb3.addItems(
            ["EULER", "NAVIER_STOKES", "WAVE_EQUATION", "HEAT_EQUATION", "FEM_ELASTICITY", "POISSON_EQUATION"])

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

        #solver
        self.t1 = QLineEdit()
        self.t2 = QLineEdit()
        self.t3 = QLineEdit()
        self.t4 = QLineEdit()
        self.t5 = QLineEdit()

        self.te = QTextEdit()

        #solver
        self.l0 = QLabel('Solver :')
        self.l1 = QLabel('Choix du schéma spacial :', self)
        self.l2 = QLabel('Choix du schéma temporel :', self)
        self.l3 = QLabel('Entrer un CFL :', self)
        self.l4 = QLabel('CFL Choisi :' + str(self.sl1.value()), self)
        self.l5 = QLabel('Mach Number :')
        self.l6 = QLabel('FREESTREAM_PRESSURE :')
        self.l7 = QLabel('FREESTREAM_Temperature :')
        self.l8 = QLabel('Charger un fichier config :')

        #Progressbar
        self.bar = QProgressBar()
        self.bar.setValue(0)
        self.bar.setMaximum(100)

        # solver
        self.Load_cfg = QPushButton("Charger un config .cfg")
        self.Load_cfg.clicked.connect(self.getConfig)
        self.Launch2 = QPushButton("Lancer SU2")
        self.Launch2.clicked.connect(self.invoke_process_popen_poll_live)

    def Tab_Post(self):
        return

    def body(self):

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
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        menuBar.addMenu('Parameters')
        menuBar.addMenu('Tools')
        menuBar.addMenu('Help')

        # Add Status Bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Current Folder Location :" + os.getcwd())




        # Creation des labels
        #maillage
        self.l11 = QLabel("Dimension du maillage :")
        self.l12 = QLabel("Nombre d'element :")
        self.l16 = QLabel('Charger un maillage : ')




        # Creation des boutons
        #maillage
        self.Load_mesh = QPushButton("Charger un maillage .su2")
        self.Load_mesh.clicked.connect(self.getMesh)
        self.Launch1 = QPushButton("Lancer GMSH")
        self.Launch1.clicked.connect(self.Click_gmsh)

        #post
        self.Launch3 = QPushButton("Lancer PARAVIEW")
        self.Launch3.clicked.connect(self.Click_paraview)

        # Creation textbox
        #maillage
        self.t11 = QLineEdit()
        self.t12 = QLineEdit()
        self.t13 = QLineEdit()



        #List
        self.list = QListView()
        # Create an empty model for the list's data
        model = QStandardItemModel(self.list)
        #model.itemChanged.connect(self.setItems)

        # Add some textual items
        foods = glob.glob("Test/*")
        print(foods)

        for food in foods:
            # Create an item with a caption
            item = QStandardItem(food)
            # Add a checkbox to it
            item.setCheckable(True)
            # Add the item to the model
            model.appendRow(item)

        def on_item_changed(item):
            # If the changed item is not checked, don't bother checking others
            if not item.checkState():
                return
            # Loop through the items until you get None, which
            # means you've passed the end of the list
            i = 0
            while model.item(i):
                if model.item(i).checkState():
                    return print(model.item(i).text())
                i += 1
        model.itemChanged.connect(on_item_changed)

        # Apply the model to the list view
        self.list.setModel(model)


        #Creation Groupbox
        self.groupbox1 = QGroupBox("Maillage :")
        self.groupbox2 = QGroupBox("Paramètre de simulation numérique :")
        self.groupbox3 = QGroupBox("Post-traitement :")
        self.groupbox4 = QGroupBox("Mode Rafale")
        self.groupbox4.setCheckable(True)
        self.groupbox4.setChecked(False)


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
        vbox1.addStretch()
        vbox1.addWidget(self.l11)
        vbox1.addWidget(self.t11)
        vbox1.addWidget(self.l12)
        vbox1.addWidget(self.t12)
        #vbox1.addWidget(self.l11)
        vbox1.addWidget(IconLabel("fa.angle-double-right", "Charger un maillage .su2 :"))
        vbox1.addWidget(self.t13)
        vbox1.addWidget(self.Load_mesh)
        vbox1.addWidget(self.Launch1)

        ### RAFALE
        vbox4 = QVBoxLayout()
        self.groupbox4.setLayout(vbox4)
        self.radiobutton = QRadioButton("Structuré")
        vbox4.addWidget(self.radiobutton)

        ### SOLVER
        vbox2 = QVBoxLayout()
        self.groupbox2.setLayout(vbox2)

        vbox2.addWidget(IconLabel("fa.wrench", "Choix du solver :"))
        #vbox2.addWidget(self.l0)
        vbox2.addWidget(self.cb3)
        #choix schema spacial
        vbox2.addWidget(self.l1)
        vbox2.addWidget(self.cb1)
        #Choix schéma temporel
        vbox2.addWidget(self.l2)
        vbox2.addWidget(self.cb2)
        ### CL
        #Mach
        vbox2.addWidget(self.l5)
        vbox2.addWidget(self.t2)
        #Pressure
        vbox2.addWidget(self.l6)
        vbox2.addWidget(self.t3)
        #Temp
        vbox2.addWidget(self.l7)
        vbox2.addWidget(self.t4)
        #Choix CFL
        vbox2.addWidget(self.l3)
        vbox2.addWidget(self.t1)
        vbox2.addStretch()
        #CFL avec slider
        #vbox2.addWidget(self.l4)
        #vbox2.addWidget(self.sl1)
        vbox2.addWidget(self.l8)
        vbox2.addWidget(self.t5)
        vbox2.addWidget(self.Load_cfg)

        vbox2.addWidget(self.checkbox1)
        vbox2.addWidget(self.checkbox2)
        vbox2.addWidget(self.checkbox3)
        vbox2.addWidget(self.Launch2)
        vbox2.addWidget(self.te)
        vbox2.addWidget(self.bar)
        vbox2.addWidget(self.groupbox4)

        ### POST
        vbox3 = QVBoxLayout()
        self.groupbox3.setLayout(vbox3)

        self.radiobutton = QRadioButton("Structuré")
        vbox3.addWidget(self.radiobutton)
        self.radiobutton = QRadioButton("Non Structuré")
        vbox3.addWidget(self.radiobutton)
        vbox3.addWidget(IconLabel("fa.file", "Fichiers output :"))
        vbox3.addWidget(self.list)
        vbox3.addStretch(1)
        vbox3.addWidget(self.Launch3)

        # Creation TAB
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)

        self.tab1 = QWidget()
        self.tabWidget.addTab(self.tab1, "Maillage")
        #self.openFile = QPushButton("Choose Tab ", self.tab1)
        self.tab1.setLayout(vbox1)

        self.tab2 = QWidget()
        self.tabWidget.addTab(self.tab2, "Paramètre de simulation numérique")
        self.tab2.setLayout(vbox2)

        self.tab3 = QWidget()
        self.tabWidget.addTab(self.tab3, "Post-traitement")
        self.tab3.setLayout(vbox3)

        self.tab4 = QWidget()
        chart = Canvas(self)
        self.tabWidget.addTab(chart, "Plot")

    def getMesh(self):
        """ This function will get the address of the file location
        """
        self.filename = QFileDialog.getOpenFileName(filter="su2 (*.su2)")[0] #argument : filter="csv (*.csv)"
        print("File :", self.filename)
        self.statusBar.showMessage("Maillage chargé : " + self.filename)
        self.t13.setText(self.filename)
        try :
            dico = Read_su2(self.filename)
        except :
            print("erreur de lectrure du maillage")
        self.t11.setText(str(dico["NDIME"]))
        self.t12.setText(str(dico["NELEM"]))

    def getFile(self):
        """ This function will get the address of the file location
        """
        self.filename = QFileDialog.getOpenFileName(filter="cfg (*.cfg)")[0] #argument : filter="csv (*.csv)"
        print("File :", self.filename)
        self.statusBar.showMessage("Maillage chargé : " + self.filename)
        self.t5.setText(self.filename)

    def getConfig(self):
        """ This function will get the address of the file location
        """
        self.filename = QFileDialog.getOpenFileName(filter="cfg (*.cfg)")[0] #argument : filter="csv (*.csv)"
        print("File :", self.filename)
        self.statusBar.showMessage("Maillage chargé : " + self.filename)
        self.t5.setText(self.filename)
        ###Permet changer la valeur d'une ComboBox
        text = "JST"
        index = self.cb1.findText(text, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.cb1.setCurrentIndex(index)

    def getITER(self):
        filename = self.t11.text()
        with open(filename) as f:
            lines = f.readlines()
        c = 0
        for line in lines:
            if "ITER" in line and c == 0:
                i = re.findall('\d+', line)[0]
                print("iteration max = ",i)
                c = 1

    def setItems(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.items.append(item)
        if item.checkState() == QtCore.Qt.Unchecked:
            self.items.remove(item)

    def print_checked_items(self):
        path = "checked.txt"
        mode = QtCore.QFile.Append if self.isWritten else QtCore.QFile.WriteOnly
        if len(self.items) > 0:
            file = QtCore.QFile(path)
            if file.open(mode):
                for item in self.items:
                    print('%s' % item.text())
                    file.write(item.text() + "\n")
            file.close()
        print("print checked items executed")

    def value_changed(self):
        self.l4.setText('CFL Choisi :' + str(self.sl1.value()))


    def selectionchange(self, i):
        print("Items in the list are :")

        for count in range(self.cb1.count()):
            print(self.cb1.itemText(count))
        print("Current index", i, "selection changed ", self.cb1.currentText())

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
        config_name = self.t5.text()
        os.system("SU2_CFD "+ config_name) #inv_NACA0012.cfg
        #ProgressBar update

    def Click_paraview(self):
        self.statusBar.showMessage('Lancement de PARAVIEW')
        file = 'C:\\Program Files\\ParaView 5.9.1-Windows-Python3.8-msvc2017-64bit\\bin\\paraview.exe'
        os.system('"' + file + '"')

    def newCall(self):
        print('New')

    def exitCall(self):
        print('Exit app')
        sys.exit(app.exec_())

    def invoke_process_popen_poll_live(self, shellType=False, stdoutType=subprocess.PIPE):
        """runs subprocess with Popen/poll so that live stdout is shown"""
        if self.t5.text() == "":
            self.statusBar.showMessage("Pas de script config")
            return
        else:
            self.statusBar.showMessage("Lancement du script")
            os.chdir("C://Users//Gameiro//Documents//CFD//SU2-master//QuickStart")
            command = "SU2_CFD "+ str(self.t5.text())  # "python OS.py"
        try:
            process = subprocess.Popen(shlex.split(command), shell=shellType, stdout=stdoutType)
        except:
            print("ERROR {} while running {}".format(sys.exc_info()[1], command))
            return None
        while True:
            output = process.stdout.readline()
            # used to check for empty output in Python2, but seems
            # to work with just poll in 2.7.12 and 3.5.2
            # if output == '' and process.poll() is not None:
            out = output.strip().decode()
            if process.poll() is not None:
                break
            if output:
                print(out)
                self.te.setText(out)
                #print("action")
                if "|       " in out:
                    try :
                        i = re.findall('\d+', out)[0]
                        #print(i)
                        self.bar.setValue(int(i))
                    except :
                        print("An exception occurred")
        rc = process.poll()
        self.statusBar.showMessage("Simulation finie")
        return rc


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


