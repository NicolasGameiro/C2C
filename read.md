<p align="center">
<img width="250" height="154" src="Common/doc/logoSU2small.png">
</p>

# C2C - Chaine 2 Calcul (ver. 0.1 "Fox"): The Open-Source Workflow simualtion in python
## Objectives
Réaliser une chaine de calcul aérodynamique avec uniquement des logiciels open-source.

Continuous Integration:<br/>
[![Regression Testing](https://github.com/su2code/SU2/workflows/Regression%20Testing/badge.svg?branch=develop)](https://github.com/su2code/SU2/actions)
[![Release](https://github.com/su2code/SU2/workflows/Release%20Management/badge.svg?branch=develop)](https://github.com/su2code/SU2/actions)

Code Quality:<br/>
[![CodeFactor](https://www.codefactor.io/repository/github/su2code/su2/badge)](https://www.codefactor.io/repository/github/su2code/su2)

Elle s'appuie sur : 
* [GMSH](https://gmsh.info/) : mailleur Open Source 
* [SU2](https://su2code.github.io/) : An open-source suite for multiphysics simulation and design from MIT
* [Paraview](https://www.paraview.org/) : Logiciel de visualisation Open Source

# C2C Installation

## Build C2C
Short summary of the minimal requirements:

- Python 3

**Note:** all other necessary build tools and dependencies are shipped with the source code or are downloaded automatically.

##  SU2 Path setup

When installation is complete, please be sure to add the `$SU2_HOME` and `$SU2_RUN` environment variables, and update your `$PATH` with `$SU2_RUN`. 

For example, add these lines to your `.bashrc` file:
```
export SU2_RUN="your_prefix/bin"
export SU2_HOME="/path/to/SU2vX.X.X/"
export PATH=$PATH:$SU2_RUN
export PYTHONPATH=$SU2_RUN:$PYTHONPATH
```

`$SU2_RUN` should point to the folder where all binaries and python scripts were installed. This is the prefix you set with the --prefix option to meson. Note that the bin/ directory is automatically added to your prefix path.

`$SU2_HOME` should point to the root directory of the source code distribution, i.e., `/path/to/SU2vX.X.X/`.

Thanks for building, and happy optimizing!

- The C2C Development Team

Tout d'abord, il faut installer un ensemble de fichiers en utilsiant la commande :
>pip install xx

Pour gagner du temps, j'ai créé un script batch qui lance l'installation de tous les package nécessaire pour cela faire :
```Bash
run pack_install.bat
pip install -r requirement.txt
```

Next

# TO DO
## Release v1.0
**date :** 06/06/2021\
Voici ce que va contenir cette release : 
* [x] Possibilité de charger un maillage .su2 pour extraire et afficher les informations suivantes :
   * [x] Dimension du maillage (1,2 ou 3)
   * [x] Nombre d'elements
* [ ] Possibilité de charger un fichier configuration .cfg pour extraire et afficher les informations suivantes :
    * [ ] Modèle
    * [ ] Schéma spatial
    * [ ] Schéma temporelle
    * [ ] Iteration max
* [ ] Il sera possible de modifier le fichier config à partir des données rentrées dans les champs (combobox et editline) de l'application
* [ ] Possibilité de lancer SU2 depuis l'application et d'afficher avec une barre de progression l'avancée du calcul
* [ ] Une barre de statut qui afficher l'état de l'application (ce qu'elle est en train de faire)
* [ ] Des tabs pour passer d'une partie à une autre (maillage, solver, post traitement)
* [ ] Une onglet Plot qui affichera l'évolution des résidus

## Release v2.0
**date :** 04/07/2021\
Contenu de la release : 
* blabla
* blabla


## Dependencies

To use these lessons, you need Python 3, and the standard stack of scientific Python: NumPy, Matplotlib, SciPy, Sympy. And of course, you need [Jupyter](http://jupyter.org)—an interactive computational environment that runs on a web browser.

This mini-course is built as a set of [Jupyter notebooks](https://jupyter-notebook.readthedocs.org/en/latest/notebook.html) containing the written materials and worked-out solutions on Python code. To work with the material, we recommend that you start each lesson with a fresh new notebook, and follow along, typing each line of code (don't copy-and-paste!), and exploring by changing parameters and seeing what happens. 

#### Without Anaconda
If you already have Python installed on your machine, you can install Jupyter using pip:

```Bash
pip install jupyter
```

Please also make sure that you have the necessary libraries installed by running

```Bash
pip install numpy scipy sympy matplotlib
```


### Running the notebook server

Once Jupyter is installed, open up a terminal and then run 

```Bash
jupyter notebook
```

## Copyright and License

(c) 2021 Gameiro Nicolas. All content is under Creative Commons Attribution [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode.txt), and all [code is under BSD-3 clause](https://github.com/engineersCode/EngComp/blob/master/LICENSE) (previously under MIT, and changed on March 8, 2018). 

We are happy if you re-use the content in any way!

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

