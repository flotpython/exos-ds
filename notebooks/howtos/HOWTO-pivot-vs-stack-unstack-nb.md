---
jupytext:
  cell_metadata_filter: all, -hidden, -heading_collapsed, -run_control, -trusted
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
  title: pivot vs stack/unstack
---

# stack / unstack et pivot

+++

## les pneus

+++

Vous vous souvenez peut-être que dans les slides on avait construit ceci :

```{code-cell} ipython3
# un code qui crée "à la main" les MultiIndex
# à des fins d'illustration seulement

import pandas as pd
import numpy as np

# index for years and visits
index = pd.MultiIndex.from_product(
    [[2013, 2014], [3, 1, 2]],
    names=['year', 'visit'])
# columns for clients and tyre pressure
columns = pd.MultiIndex.from_product(
    [['Bob', 'Sue'], ['Front', 'Rear']],
    names=['client', 'tyre pressure'])

# mock some data
data = 2 + np.random.rand(6, 4)

# create the DataFrame
mechanics_data = pd.DataFrame(data, index=index, columns=columns)

mechanics_data
```

## générons les données

+++

dans ce premier code nous avons créé les données directement dans la bonne forme

mais en pratique ce qu'on fournit en général c'est plutôt une table qui ressemble à ceci

```{code-cell} ipython3
# voici comment on pourrait produire une table
# qui serait plus conforme à la réalité

from itertools import product

names = ['Bob', 'Sue']
years = list(range(2013, 2015))
visits = list(range(1, 4))
tyres = ['Front', 'Rear']

# une compréhension de liste
data = [
    # qui contient un dictionnaire par ligne
    dict(name=name, year=year, visit=visit, tyre=tyre, 
         # ici on évite le coté "random" en incrémentant
         # un peu à chaque pas; la pression est entre 2 et 3
         pressure=2+index/25)
    # 
    for index, (name, year, visit, tyre) in 
    # product pour parcourir le produit cartésien
    # sur les 4 dimensions
    enumerate(product(names, years, visits, tyres))
]
```

```{code-cell} ipython3
df = pd.DataFrame(data)
df
```

## `pivot_table`

+++

typiquement la table du début, on l'aurait créée à partir des données brutes comme ceci

```{code-cell} ipython3
pivot = df.pivot_table(
    values='pressure',
    index=['year', 'visit'],
    columns=['name', 'tyre'])
pivot
```

## stack/unstack

+++

### `unstack()`

+++

`unstack()` va faire migrer un étage de l'index des colonnes (ici on a deux niveaux year et visit) vers l'espace des colonnes

```{code-cell} ipython3
# unstack : on part de la dimension des lignes
# et dans cette dimension notre multi-index contient
# 0: year
# 1: visit (donc aussi -1 car le dernier)
unstacked = pivot.unstack(level=-1)
unstacked
```

### `stack()`

+++

toujours à partir de la forme carrée 2x2 issue du pivot, dans l'autre sens, `stack()` va faire...

```{code-cell} ipython3
# ici stack part des colonnes vers les index
# donc les niveaux sont
# 0: name
# 1: tyre

# remarquez que je peux aussi bien utiliser le nom
# et que c'est sans doute préférable

stacked = pivot.stack(level='tyre')
stacked
```

### à la limite

+++

si je persiste, en faisant encore une fois `stack()`, j'obtiens cette fois .. une série

```{code-cell} ipython3
# ici stack part des colonnes vers les index
# donc les niveaux sont
# 0: name
# 1: tyre

# donc level=-1 désigne le niveau 'tyre'
stacked2 = pivot.stack().stack()
type(stacked2)
```

et donc si vous avez suivi, le nombre de niveau dans l'index de cette série, c'est ?

```{code-cell} ipython3
len(stacked2.index.levels)
```

## produire le pivot à la main

+++

voyons maintenant comment on pourait produire le pivot sans passer par `pivot_table()`, et donc de manière plus pédestre, en gérant nous mêmes les `index` et les `unstack()`

c'est surtout pour le sport bien sûr, pour bien comprendre.

```{code-cell} ipython3
# on repart de la donnée brute
df.head()
```

la première chose à faire est donc de mettre les catégories en index

```{code-cell} ipython3
# et pour ça on peut faire par exemple
df_1column = df.set_index(['name', 'year', 'visit', 'tyre'])
df_1column.head()
```

et là, il ne me reste plus qu'à faire quoi ?

+++

***
***
***

+++

je vous laisse réfléchir...

+++

***
***
***

```{code-cell} ipython3
# ça marche pas trop mal, mais pas exactement
# car si je ne précise rien je vais avoir un arrangement
# qui dépend de l'ordre des niveaux dans l'index
# (unstack sans argument prend l'index=-1)

df_1column.unstack().unstack()
```

```{code-cell} ipython3
df_1column.unstack("name").unstack("tyre")
```
