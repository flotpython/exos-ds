---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
  encoding: '# -*- coding: utf-8 -*-'
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -language_info.version, -language_info.codemirror_mode.version, -language_info.codemirror_mode,
    -language_info.file_extension, -language_info.mimetype, -toc
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  nbconvert_exporter: python
  pygments_lexer: ipython3
nbhosting:
  show_up_down_buttons: true
  title: mosaique pandas
---

*Quand les exercices font partie d'une série d'exercices, faites les dans l'ordre, ils se servent des précédents...**

+++

# mosaique (un peu de tout)

+++

Importer `numpy` et `pandas`  indiquer la version des bibliothèques

```{code-cell} ipython3
# votre code ici
```

Importer `pyplot` de `matplotlib` et  mettez les plots en mode `notebook`

```{code-cell} ipython3
# votre code ici
```

**[note importante]**  
avec le mode `notebook`, il est souvent utile de déclarer explicitement que la cellule va produire une figure avec
`plt.figure()` (ou autre fonction qui crée une figure ou des sous-figures)  
sinon votre dessin va être inséré dans la dernière figure ouverte, souvent c'est plus haut dans le notebook...

```python
# par exemple, faites
plt.figure()
# avant de faire 
plt.plot(X, Y)
# ...
```

+++

# Exercices sur la suite de Syracuse

+++

## La suite de Syracuse

pour chaque $n\in \mathbb{N^*}$, on définit une suite de Syracuse par:
   - $u_0 = n$
   - $u_{p+1}={\begin{cases}{\dfrac {u_{p}}{2}}&{\mbox{si }}u_{p}{\mbox{ est pair,}}\\3u_{p}+1&{\mbox{si }}u_{p}{\mbox{ est impair.}}\end{cases}}$

+++

### Les consignes

   1. la suite s'arrête après le premier $1$
   1. lever une exception si le type de l'argument n'est pas valide (*TypeError*), pensez à utiliser `isinstance`
   1. lever une exception si la valeur de l'argument n'est pas valide (*ValueError*)
   - pensez à mettre un message explicatif dans vos exceptions
   1. mettez un docstring à la fonction

+++

### Implémentation de la suite de Syracuse
   
   - implémenter une fonction **syracuse** qui retourne la liste de la suite des nombres de Syracuse pour un $u_0$ donné sous les conditions précédentes

+++

par exemple
```python
>>> syracuse(10)
[10, 5, 16, 8, 4, 2, 1]
```

+++

     
**Exécutions**:
   - tester votre fonction dans les cas suivants (n vaut 0, "toto", 4 et 27) en rattrapant les exceptions levées

```{code-cell} ipython3
# EXERCICE
def syracuse(n):
    # votre code ici
    pass
```

```{code-cell} ipython3
# pour vérifier
syracuse(10) == [10, 5, 16, 8, 4, 2, 1]
```

```{code-cell} ipython3
# pour vérifier
try:
    syracuse("toto")
except TypeError:
    print("OK your code raises TypeError on a str")
```

```{code-cell} ipython3
# pour vérifier
try:
    syracuse(-12)
except ValueError:
    print("OK your code raises TypeError on a str")
```

## Plotter la suite de Syracuse

**[indications]:**
   - attention les sous-figures sont appelées *axis* en matplotlib.pyplot

+++

**[rappels]:**
  - une figure peut être composée de sous-figures
  - les sous-figures sont appelées des *Axis* (pensez toujours: axis = subfigure)

+++

   - créer une figure globale de titre *syracuse*
   - créer six sous-figures en une grille de 2 lignes et 3 colonnes en plottant 6 suites de syracuse - par exemple pour les entrées 4, 8, 12, 5, 10 et 20
   - donner la même taille aux sous-figures
   - donner un titre aux sous-figures

```{code-cell} ipython3
inputs = (4, 8, 12, 5, 10, 20)
```

```{code-cell} ipython3
# à vous

...
```

# Exercice: vectorization de fonctions

+++

   - implémenter la fonction valeur absolue sans utiliser `numpy.abs` ni aucune fonction numpy dans le corps de la fonction
   - créer un `numpy.ndarray` contenant des flottants linéairement espacés entre -100 et 100
   - appliquez votre fonction à ce tableau
   - quel problème constatez-vous ?

+++

**[indications]**


   - si vous voulez que votre fonction ($abs: float \rightarrow float)$ puisse s'appliquer à des tableaux numpy
   - il faut la vectoriser en utilisant le décorateur `numpy.vectorize`

```{code-cell} ipython3
# votre code ici

def abs (n):
    # votre code ici
    pass

# votre code ici
# x = ...
# abs(x)
# pensez à rattraper l'erreur
```

# 3D plotting

+++

   - implémentez en utilisant les opérateurs et fonctions numpy une fonction (dans le genre de) $f(x, y) = x^2 + y^2$ 
   - plotter votre fonction en 3D

```{code-cell} ipython3
# votre code ici
```

# Travail sur des fichiers `csv`

+++

**[consigne]**
   - ne pas utiliser de boucles python sur les tableaux *csv*

+++

## Lecture de fichiers csv

+++

### Lecture d'un (petit) csv sans noms de colonnes
   - créer une *pandas.DataFrame* *df1* à partir du (petit) fichier `data/weight_height_no_names.csv`
   - il ne comporte pas de noms de colonnes
   - passer lui la liste des colonnes =["genre", "taille", "poids"] à la création de la DataFrame
   - afficher la taille de la DataFrame

```{code-cell} ipython3
# à vous
df1 = ...
```

```{code-cell} ipython3
:cell_style: split
:lines_to_next_cell: 2

df1
```

```{code-cell} ipython3
:cell_style: split
:tags: [raises-exception]

# ceci doit afficher True
df1.shape == (7, 3)
```

###  Lecture d'un (petit) csv avec des lignes de commentaires mais sans noms de colonnes 
   - créer une *pandas.DataFrame* *df2* à partir du (petit) fichier `data/weight_height_no_comments.csv`
   - les valeurs sont séparées par des ';'
   - ce fichier comporte 3 lignes de commentaires
   - il ne comporte pas de noms de colonnes
   - mettez dans la DataFrame existante la liste de colonnes: ["Gender", "Height", "Weight"]

```{code-cell} ipython3
# le contenu du fichier 

%cat data/weight_height_no_comments.csv
```

```{code-cell} ipython3
# à vous
df2 = ...
```

```{code-cell} ipython3
:cell_style: center
:tags: [raises-exception]

# ceci doit afficher True
(
    df2.shape == (9, 3)
and df2.columns[0] == 'Gender'
)
```

### Lecture d'un (gros) fichier csv avec le nom des colonnes et sans commentaires
   - créer une *pandas.DataFrame* *df* à partir du (gros) fichier `data/weight_height.csv`
   - les valeurs sont séparées par des ';'
   - la première ligne comporte le nom des colonnes
   - cette DataFrame servira dans les fonctions suivantes

```{code-cell} ipython3
# votre code ici
df = ...
```

```{code-cell} ipython3
:cell_style: split
:tags: [raises-exception]

df.head()
```

```{code-cell} ipython3
:cell_style: split
:tags: [raises-exception]

# ceci doit afficher True
(
    df.shape == (10000, 3)
and df.columns[0] == 'Gender'
)
```

## Informations générales sur une DataFrame

on veut en savoir plus sur cette DataFrame *df* précédente

+++

affichez les types des colonnes

```{code-cell} ipython3
# à vous
```

+++ {"tags": ["level_basic"]}

affichez un résumé / des informations générales

```{code-cell} ipython3
# à vous
```

## Manipulations des colonnes de la DataFrame

+++

### Conversions

- convertissez les tailles de *inches* à *mètres* ($cm = in \times 2.54$)
- convertissez les poids de *pounds* à *kg* ($kg = \dfrac{lb}{2.2046}$)

```{code-cell} ipython3
# votre code ici 
# et n'hésitez pas à recharger le fichier
# pour partir d'un truc propre

...
# df.head()
```

### Ajout d'une colonne

- calculer l'indice de masse corporelle $ i = \frac{weight}{height^2} $  
  et rangez-le dans une colonne `Mass Index` de la DataFrame

```{code-cell} ipython3
# votre code ici n'hésitez pas à recharger le fichier
# pour partir d'un truc propre

df = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

df.head()
```

###  Catégorisation
  
* ajouter une colonne "Gender-cat" dans laquelle le genre a été catégorisé (le type de la colonne doit être `category`)
* en option, renommez les termes de cette catégorie en minuscules `male` et `female`

```{code-cell} ipython3
# votre code ici n'hésitez pas à recharger le fichier
# pour partir d'un truc propre

# df = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

df.head()
```

```{code-cell} ipython3
:tags: [raises-exception]

df.dtypes
```

### Calculs sur une colonne

+++

- compter le nombre de valeurs différentes dans la colonne "Gender"

```{code-cell} ipython3
# à vous
```

- calculez la moyenne du poids

```{code-cell} ipython3
# à vous
```

- et l'écart-type de l'indice de masse corporelle

```{code-cell} ipython3
# à vous
```

## Plots de colonnes de la DataFrame

+++

###   Les boxplots
   1. tracer le *boxplot* de la colonne *height*

   1. tracer le *boxplot* de la colonne *weight*

```{code-cell} ipython3
# à vous
```

### Les femmes par poids

+++

* tracer les tailles des femmes en fonction de leurs poids

```{code-cell} ipython3
# à vous
```

### Tri de colonnes et plots

+++

* trier les tailles en ordre croissant et plotter les

```{code-cell} ipython3
# à vous
```

* plotter sur une même figure les tailles par genre

```{code-cell} ipython3
# à vous
```

* afficher en ordre croissant les personnes de plus de 180 cm

```{code-cell} ipython3
# à vous
```

# NaN

+++

## Lecture du csv

+++

* lisez le fichier `data/car_sales.csv` (la première ligne contient le nom des colonnes)

```{code-cell} ipython3
# à vous de jouer

cars = ...
```

```{code-cell} ipython3
:hide_input: false
:tags: [raises-exception]

cars.head(5)
```

+++ {"hide_input": false}

* le nombre de lignes dans la dataframe

```{code-cell} ipython3
# votre code
```

+++ {"hide_input": false}

* nombre de colonnes dans la dataframe

```{code-cell} ipython3
# à vous
```

* afficher les colonnes

```{code-cell} ipython3
# à vous de jouer
```

* afficher les lignes 10 à 14 inclusivement (on compte à partir de 1)

```{code-cell} ipython3
# à vous de jouer
```

##   Nombres de NaN

+++

* le nombre de NaN par colonne (sans boucle python)

```{code-cell} ipython3
# votre code
```

+++ {"hide_input": false}

* le nombre de NaN par ligne

```{code-cell} ipython3
# à vous de jouer
```

## Suppression de NaN

+++

- supprimer les colonnes qui ont plus de $5$ NaN 

**indices**
* la taille originale de notre dataframe est 157 lignes et 16 colonnes
* voyez `pandas.dropna`
* ça concerne une colonne

```{code-cell} ipython3
# votre code ici
```

- supprimer les lignes qui ont plus de $5$ NaN

  ça devrait concerner une ligne

```{code-cell} ipython3
# votre code ici
```

- supprimer les lignes qui ont au moins un NaN

```{code-cell} ipython3
# votre code ici
```

- supprimer les colonnes qui ont au moins un NaN

```{code-cell} ipython3
# votre code ici
```
