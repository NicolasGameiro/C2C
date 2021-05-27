"""
Author : GAMEIRO Nicolas

Description :
Script pour lire les fichiers .su2 de maillage et .cfg de configuration de la simulation

Contenu :
- fct : Read_cfg(filename)
- fct : Read_su2(filename)
- fct : Read_res(filename)

Date Creation : 27/05/2021
Last Update : 27/05/2021
"""

### Import
import re
import pandas as pd

### Fonctions

def Read_cfg(filename):
    filename = "test.cfg.txt"
    with open(filename) as f:
        lines = f.readlines() #Cree une liste avec chaque element correspond à une ligne du file
    #Il suffit de connaitre le numéro de la ligne à réécrire et d'aller la chercher dans la liste (attention python démarre à 0)
    dico = {"SOLVER" : 16, "MACH_NUMBER" : 26, "FREESTREAM_PRESSURE" : 33, "FREESTREAM_TEMPERATURE" : 36, "CFL_NUMBER" : 97, "ITER" : 107, "MGLEVEL" : 126, "CONV_NUM_METHOD_FLOW" : 150, "MUSCL_FLOW" : 154, "TIME_DISCRE_FLOW" : 164 }
    print(lines)
    Info = {"SOLVER=" : "EULER", "MACH_NUMBER=" : "0.3", "FREESTREAM_PRESSURE=" : "102050", "FREESTREAM_TEMPERATURE=" : "300", "CFL_NUMBER=" : "500", "ITER=" : "1000", "MGLEVE=" : "0", "CONV_NUM_METHOD_FLOW=" : "ROE", "MUSCL_FLOW=" : "NO", "TIME_DISCRE_FLOW=" : "RUNGE-KUTTA_EXPLICIT" }
    newlines = lines
    print("#############################################")
    print("########## Modification des lignes ##########")
    print("#############################################")
    L1 = list(Info.keys())
    L2 = list(Info.values())
    for i in range(len(Info.keys())):
        info = L1[i] + L2[i]
        print(info)
    c = 0
    for value in dico.values():
        newlines[value] = info[c]
        print(newlines[value])
        c = c + 1

def Read_su2(filename,dico_ref={}):
    #Test
    Test = 0
    if Test == 1:
        filename = "C:\\Users\\Gameiro\\Documents\\CFD\\SU2-master\\QuickStart\\mesh_NACA0012_inv.su2"
        dico_ref = {"NDIME" : 2, "NELEM" : 10216, "NPOIN" : 5233, "NMARK" : 2, "MARKER_TAG" : "airfoil", "MARKER_ELEMS" : 200 }

    dico = {"NDIME" : 1, "NELEM" : 106, "NPOIN" : 53, "NMARK" : 4, "MARKER_TAG" : "airefoil", "MARKER_ELEMS" : 400 }

    print(filename)
    #Script
    with open(filename) as f:
        lines = f.readlines() #Cree une liste avec chaque element correspond à une ligne du file

    for key in dico.keys():
        c = 0 #Compteur permet de s'arreter quand on trouve la première occurence d'un parametre
        for line in lines:
            if key in line and c == 0:
                try :
                    #print(re.findall('\d+', line))
                    i = re.findall('\d+', line)[0]
                    i = int(i)
                except :
                    split_value = line.find("=")
                    i = line[split_value+1:-1]
                #print(key,"=", i)
                c = 1
            dico[key] = i
    return dico
#print("Info maillage ==> ",Read_su2("test.txt"))

def Read_res(filename):
    res = pd.read_csv(filename)
    Name = list(res.head(0))
    print(Name)
    it = list(res[Name[2]][:])
    rms_ro = list(res[Name[3]][:])
    rms_rou = list(res[Name[4]][:])
    rms_rov = list(res[Name[5]][:])
    rms_roe = list(res[Name[6]][:])

    Res = [it,rms_ro,rms_rou,rms_rov,rms_roe]
    return Res
#filename = "Test/history.csv"
#Residus(filename)




