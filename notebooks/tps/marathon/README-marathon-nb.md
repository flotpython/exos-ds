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
  title: exo marathon
---

# marathon (divers basique)

+++

pour réaliser ce TP localement sur votre ordi, {download}`commencez par télécharger le zip<./ARTEFACTS-marathon.zip>`

+++

un petit TP pour travailler

* le chargement et la sélection
* un peu de groupby
* un peu de gestion du temps et des durées

+++ {"tags": []}

# outils

```{code-cell} ipython3
import pandas as pd
```

on utilise ici un utilitaire pour regarder le début d'un fichier texte

```{code-cell} ipython3
# sur les plateformes Unix on peut faire simplement
# 
# ! head -5 data/marathon.txt
#
# mais sur Windows ça ne fonctionne pas, alors...

from head import head

help(head)
```

# TP: une dataframe simple

+++

On va étudier un jeu de données trouvé sur Internet

```{code-cell} ipython3
URL = "http://www.xavierdupre.fr/enseignement/complements/marathon.txt"
```

## chargement

+++

Le premier réflexe pour charger un fichier de ce genre, c'est d'utiliser la fonction `read_csv` de pandas

```{code-cell} ipython3
# votre cellule de code
# qu'on va faire descendre
# et raffiner au fur et à mesure

df0 = pd.read_csv(URL)
df0.head()
```

c'est un début, mais ça ne marche pas franchement bien !

+++

il faut donc bien regarder la doc

```{code-cell} ipython3
# pd.read_csv?
```

+++ {"tags": ["level_basic"]}

et pour commencer je vous invite à préciser le séparateur:

```{code-cell} ipython3
# à vous de modifier cette première approche

df1 = pd.read_csv(URL)
```

```{code-cell} ipython3
# pour vérifier, ceci doit afficher True
df1.shape == (358, 4) and df1.iloc[0, 0] == 'PARIS' and df1.columns[0] == 'PARIS'
```

c'est mieux, mais les noms des colonnes ne sont pas corrects

en effet par défaut, `read_csv` utilise la première ligne pour déterminer les noms des colonnes

or dans le fichier texte il n'y a pas le nom des colonnes !

```{code-cell} ipython3
# NOTE: si vous n'avez pas le module head, ouvrez le fichier dans votre éditeur favori

head("data/marathon.txt", 5)
```

+++ {"tags": ["level_basic"]}

du coup ce serait pertinent de donner un nom aux colonnes

```{code-cell} ipython3
NAMES = ["city", "year", "duration", "seconds"]
```

```{code-cell} ipython3
# à vous de créer une donnée bien propre
df = ... # pd.read_csv(URL)
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier, ceci doit afficher True
df.shape == (359, 4) and df.iloc[0, 0] == 'PARIS' and df.columns[0] == 'city'
```

```{code-cell} ipython3
:tags: [raises-exception]

# ce qui maintenant nous donne ceci
df.head(2)
```

## sauvegarde dans un fichier csv

+++

dans l'autre sens quand on a produit une dataframe et qu'on veut sauver le résultat dans un fichier texte

```{code-cell} ipython3
# df.to_csv?
```

par exemple je crée ici un fichier qu'on peut relire sous excel

```{code-cell} ipython3
:hide_input: false
:tags: [raises-exception]

loop = "marathon-loop.csv"
df.to_csv(loop, sep=";", index=False)
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour voir un aperçu
head(loop, 4)
```

## des recherches

+++

### les éditions de 1971

```{code-cell} ipython3
# à vous de calculer les éditions de 1971
df_1971 = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# ceci doit retourner True
df_1971.shape == (3, 4) and df_1971.seconds.max() == 8574
```

+++ {"tags": ["level_basic"]}

### l'édition de 1981 à Londres

```{code-cell} ipython3
# à vous
df_london_1981 = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# ceci doit retourner True
df_london_1981.shape == (1, 4) and df_london_1981.iloc[0].seconds == 7908
```

### trouver toutes les villes

+++ {"tags": ["level_basic"]}

on veut construire une collection de toutes les villes qui apparaissent au moins une fois

```{code-cell} ipython3
# à vous

cities = ...
```

```{code-cell} ipython3
# intéressez-vous au type du résultat

# la version la plus naïve retourne un ndarray
import numpy as np

isinstance(cities, np.ndarray)
```

## des extraits

```{code-cell} ipython3
# attention mes numéros de ligne commencent à 1
head("data/marathon.txt", 12)
```

### extrait #1

+++ {"tags": ["level_basic"]}

les entrées correspondant aux lignes 10 à 12 inclusivement

```{code-cell} ipython3
# à vous
df_10_to_12 = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# ceci doit retourner True
df_10_to_12.shape == (3, 4) and df_10_to_12.iloc[0].year == 2002 and df_10_to_12.iloc[-1].year == 2000
```

### extrait #2

+++ {"tags": ["level_basic"]}

une Series correspondant aux événements à Paris après 2000 (inclus), 
dans laquelle on n'a gardé que l'année

```{code-cell} ipython3
# à vous
s_paris_2000 = ...
```

```{code-cell} ipython3
s_paris_2000
```

```{code-cell} ipython3
:tags: [raises-exception]

# ceci doit retourner True
isinstance(s_paris_2000, pd.Series) and len(s_paris_2000) == 12 and s_paris_2000.iloc[-1] == 2000
```

### extrait #3

+++ {"tags": ["level_basic"]}

une DataFrame correspondant aux événements à Paris après 2000, 
dans laquelle on n'a gardé que les deux colonnes `year` et `seconds`

```{code-cell} ipython3
df_paris_2000_ys = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# ceci doit retourner True
(isinstance(df_paris_2000_ys, pd.DataFrame)
 and df_paris_2000_ys.shape == (12, 2) 
 and df_paris_2000_ys.iloc[-2].seconds == 7780)
```

+++ {"hide_input": true, "tags": []}

## aggrégats

+++ {"tags": []}

### moyenne

+++ {"tags": ["level_basic"]}

ce serait quoi la moyenne de la colonne `seconds` ?

```{code-cell} ipython3
# calculer la moyenne de la colonne 'seconds'

seconds_average = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier
import math
math.isclose(seconds_average, 7933.660167130919)
```

****

```{code-cell} ipython3
# en guise de révision de Python, transformez cette valeur en chaine
# au format 2h 12' 13''

formatted_average = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier
formatted_average == "2h 12' 13''"
```

### combien de marathons par an

+++ {"hide_input": false, "tags": ["level_basic"]}

si maintenant je veux produire une série qui compte par année combien il y a eu de marathons

```{code-cell} ipython3
# à vous

count_by_year = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier
(isinstance(count_by_year, pd.Series)
 and len(count_by_year) == 65
 and count_by_year.loc[1947] == 1
 and count_by_year.loc[2007] == 9
 and count_by_year.loc[2011] == 5)
```

## les durées

+++ {"tags": ["level_intermediate"]}

dans cette partie, notre but est de simplement vérifier que la colonne `seconds` contient bien le nombre de secondes correspondant à la colonne `duration`

+++

pour cela on va commencer par convertir la colonne `duration` en quelque chose d'un peu plus utilisable

`numpy` expose deux types particulièrement bien adaptés à la gestion du temps

* `datetime64` pour modéliser un instant particulier
* `timedelta64` pour modéliser une durée entre deux instants

voir plus de détails si nécessaire ici: <https://numpy.org/doc/stable/reference/arrays.datetime.html>

+++

### `read_csv(parse_dates=)`

+++

commençons par écarter une fausse bonne idée

dans `read_csv` il y a une option `parse_dates`; mais regardez ce que ça donne

```{code-cell} ipython3
df_broken = pd.read_csv(URL, sep='\t', 
                        names=['city', 'year', 'duration', 'seconds'], 
                        parse_dates=['duration'])
df_broken
```

**ça ne va pas !**

le truc c'est que ici, on n'a **pas une date** mais c'est une **durée**

```{code-cell} ipython3
:tags: [raises-exception]

# repartons des données de départ

df.dtypes
```

+++ {"tags": ["level_basic"]}

non, pour convertir la colonne en `datetime64` on va utiliser `pd.to_timedelta`

voyez la documentation de cette fonction, et modifiez la dataframe `df` pour que la colonne `duration` soit maintenant du type `timedelta64`

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier - doit retourner True
df.duration.dtype == 'timedelta64[ns]'
```

```{code-cell} ipython3
:tags: [raises-exception]

# et effectivement c'est beaucoup mieux

df.head(2)
```

### duration == seconds ?

+++

à présent qu'on a converti `duration` dans le bon type, on peut utiliser toutes les fonctions disponibles sur ce type.  
en pratique ça se fait en deux temps

* sur l'objet `Series` on applique l'attribut `dt` pour, en quelque sorte, se projeter dans l'espace des 'date-time', exactement comme on l'a vu déjà avec le `.str` lorsqu'on a besoin d'appliquer des méthodes comme `.lower()`  
  plus de détails ici <https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.html>
* de là on peut appeler toutes les méthodes disponibles sur les objets `timedelta` - on pourra en particulier s'intéresser à `total_seconds`

+++ {"tags": ["level_basic"]}

du coup pour vérifier que la colonne `seconds` correspond bien à `duration`, on écrirait quoi comme code (qui doit afficher `True`)

```{code-cell} ipython3
# à vous
```

+++ {"tags": ["level_basic"]}

on se propose maintenant de rajouter des colonnes `hour` `minute` et `second` - qui doivent être de type entier

**indices**
* on peut calculer le quotient et le reste entre deux objets `timedelta` avec les opérateurs usuels `//` et `%`
* on peut construire un objet `timedelta` comme par exemple `timedelta(hours=1)`

```{code-cell} ipython3
from datetime import timedelta
```

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
:tags: [raises-exception]

# pour vérifier
(    np.all(df.loc[0, ['hour', 'minute', 'second']] == [2, 6, 29])
 and df.hour.dtype == int
 and df.minute.dtype == int 
 and df.second.dtype == int)
```

***
