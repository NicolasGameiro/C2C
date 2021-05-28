"""
Author : GAMEIRO Nicolas

Description :
Script pour lire les fichiers .su2 de maillage et .cfg de configuration de la simulation

Contenu :
- fct : Read_cfg(filename)
- fct : Read_su2(filename)
- fct : Read_res(filename)
- fct : Write_cfg(filename,dico)
- fct : Write_su2(filename,dico)
- fct : Read_res(filename)

Date Creation : 27/05/2021
Last Update : 28/05/2021
"""

### Import
import re
import pandas as pd

### Fonctions
def Write_su2(filename):
    # Test
    Test = 1
    if Test == 1:
        if Test == 1:
            filename = "C:\\Users\\s611962\\PycharmProjects\\pythonProject\\C2C-main\\Test\\mesh_NACA0012_inv.su2"
            dico_ref = {"NDIME=": "2", "NELEM=": "10216", "NPOIN=": "5233", "NMARK=": "2", "MARKER_TAG=": "airfoil",
                        "MARKER_ELEMS=": "200"}

    # Script
    with open(filename) as f:
        lines = f.readlines()  # Cree une liste avec chaque element correspond à une ligne du file
    newlines = lines
    print("\n#############################################")
    print("########## Creation des newlines ##########")
    print("#############################################\n")
    L1 = list(dico_ref.keys())
    L2 = list(dico_ref.values())
    info = []
    for i in range(len(dico_ref.keys())):
        info.append(L1[i] + " " + L2[i] + "\n")
        print(info[i])
    print(info)

    print("\n#############################################")
    print("########## Modification des lignes ##########")
    print("#############################################\n")
    j = 0  # compteur liste info
    for key in dico_ref.keys():
        c = 0  # Compteur permet de s'arreter quand on trouve la première occurence d'un parametre
        i = -1  # Numéro de la ligne qu'on regarde
        for line in newlines:
            i += 1
            if key in line and c == 0:
                print("On regarde la ligne ", i)
                print("Ancienne ligne ==> ",line)
                try:
                    newlines[i] = info[j]
                    print("La nouvelle ligne vaut ==> ",newlines[i])
                except:
                    print("Erreur d'écriture de la ligne")
                c = 1
        j += 1
    # On réécrit avec newlines dans le fichier config
    with open("new_mesh.su2", "w") as f:
        f.writelines(newlines)
    return newlines

def Write_cfg(filename,dico={}):
    # Test
    Test = 1
    if Test == 1:
        filename = "C:\\Users\\s611962\\PycharmProjects\\pythonProject\\C2C-main\\Test\\inv_NACA0012.cfg"
        dico_ref = {"SOLVER=": "EULER", "MACH_NUMBER=": "0.3", "FREESTREAM_PRESSURE=": "102050",
                    "FREESTREAM_TEMPERATURE=": "300", "CFL_NUMBER=": "500", "ITER=": "1000", "MGLEVE=": "0",
                    "CONV_NUM_METHOD_FLOW=": "ROE", "MUSCL_FLOW=": "NO", "TIME_DISCRE_FLOW=": "RUNGE-KUTTA_EXPLICIT"}

    #Script
    with open(filename) as f:
        lines = f.readlines() #Cree une liste avec chaque element correspond à une ligne du file
    newlines = lines
    print("\n#############################################")
    print("########## Creation des newlines ##########")
    print("#############################################\n")
    L1 = list(dico_ref.keys())
    L2 = list(dico_ref.values())
    info = []
    for i in range(len(dico_ref.keys())):
        info.append(L1[i] + " "+ L2[i] + "\n")
        print(info[i])
    print(info)

    print("\n#############################################")
    print("########## Modification des lignes ##########")
    print("#############################################\n")
    j = 0  # compteur liste info
    for key in dico_ref.keys():
        c = 0 #Compteur permet de s'arreter quand on trouve la première occurence d'un parametre
        i = -1 #Numéro de la ligne qu'on regarde
        for line in newlines:
            i += 1
            if key in line and c == 0:
                #print("On regarde la ligne ", i)
                #print("Ancienne ligne ==> ",line)
                try :
                    newlines[i] = info[j]
                    #print("La nouvelle ligne vaut ==> ",newlines[i])
                except :
                    print("Erreur d'écriture de la ligne")
                c = 1
        j += 1
    #On réécrit avec newlines dans le fichier config
    with open("new_cfg.cfg","w") as f:
        f.writelines(newlines)
    return newlines

def Read_cfg(filename):
    # Test
    Test = 0
    if Test == 1:
        filename = "C:\\Users\\s611962\\PycharmProjects\\pythonProject\\C2C-main\\Test\\inv_NACA0012.cfg"
        dico_ref = {"SOLVER=": "EULER", "MACH_NUMBER=": "0.3", "FREESTREAM_PRESSURE=": "102050",
                    "FREESTREAM_TEMPERATURE=": "300", "CFL_NUMBER=": "500", "ITER=": "1000", "MGLEVE=": "0",
                    "CONV_NUM_METHOD_FLOW=": "ROE", "MUSCL_FLOW=": "NO", "TIME_DISCRE_FLOW=": "RUNGE-KUTTA_EXPLICIT"}

    dico = {"SOLVER": 16, "MACH_NUMBER": 26, "FREESTREAM_PRESSURE": 33, "FREESTREAM_TEMPERATURE": 36, "CFL_NUMBER": 97,
            "ITER": 107, "MGLEVEL": 126, "CONV_NUM_METHOD_FLOW": 150, "MUSCL_FLOW": 154, "TIME_DISCRE_FLOW": 164}

    # Script
    with open(filename) as f:
        lines = f.readlines()  # Cree une liste avec chaque element correspond à une ligne du file

    for key in dico.keys():
        c = 0  # Compteur permet de s'arreter quand on trouve la première occurence d'un parametre
        for line in lines:
            if key in line and c == 0:
                try:
                    # print(re.findall('\d+', line))
                    i = re.findall('\d+', line)[0]
                    i = int(i)
                except:
                    split_value = line.find("=")
                    i = line[split_value + 1:-1]
                # print(key,"=", i)
                c = 1
            dico[key] = i
    return dico

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

if __name__ == '__main__':
    print("Info maillage ==> ",Read_su2("test.txt"))
    #print("Info config ==> ",Read_cfg("test.txt"))
    #print("New config ==> ",Write_cfg("test.txt"))
    #print("New mesh su2 ==> ", Write_su2("test.txt"))
    #filename = "Test/history.csv"
    #Residus(filename)