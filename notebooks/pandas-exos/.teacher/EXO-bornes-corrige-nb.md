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
  title: exo bornes
---

# `stack()` pour énumérer une liste

```{code-cell} ipython3
import pandas as pd
from head import head
```

```{code-cell} ipython3
# pour information seulement (on a des .csv maintenant)
# pour lire les excel au format .xlsx il faut importer ceci

# !pip install openpyxl
```

on a trois tables comme ceci

```{code-cell} ipython3
df1 = pd.read_csv('data/bornes.csv', sep=';')
df2 = pd.read_csv('data/bornes2.csv', sep=';')
df3 = pd.read_csv('data/bornes3.csv', sep=';')
```

```{code-cell} ipython3
:cell_style: split

df1
```

```{code-cell} ipython3
:cell_style: split

df2
```

```{code-cell} ipython3
df3
```

on veut transformer cela pour aboutir à ceci; une ligne par borne

| ville | borne | op_name |
|-|-|-|
| Paris | 201 | Tesla |
| Paris | 202 | City EV| 
|...| ...| ...|

+++

il s'agit donc de démêler l'écheveau pour fabriquer une table qui a 6 lignes, et pour chaque ligne l'opérateur de la borne

+++

## indices

* on a vu dans le cours que sur un objet Series on pouvait avoir besoin
  occasionnellement d'utiliser l'attribut `str`
* ici on a envie de passer par un objet liste; notamment je vous rappelle
  * la méthode `replace()` sur les chaines de caractères
  * la méthode `split()` sur les chaines de caractères
* une fois que vous êtes arrivés à mettre une liste dans une cellule d'une Series, 
  il peut être intéressant de remplacer ce contenu par .. un objet Series
* vous pourrez ensuite invoquer la méthode `.stack()` sur la Series englobante

+++

----

```{code-cell} ipython3
# à vous de jouer
# prune-begin-next
```

## on coupe en morceaux

```{code-cell} ipython3
s = (df1.bornes
    # ça a l'air compliqué mais en fait non:
    # on manipule la chaine [201, 202] 
    .str.replace('[', '', regex=False)  # pour enlever les [ puis les ] puis les espaces
    .str.replace(']', '', regex=False)
    .str.replace(' ', '', regex=False)
    # puis là on découpe la chaine selon les ,
    .str.split(',')
    # ici on a une liste, on l'utilise pour créer une Series
    .apply(pd.Series)
    # et c'est là que s'exerce la magie de stack()
    #  on rajoute un étage dans l'index
    .stack())
```

```{code-cell} ipython3
s
```

## des entiers

```{code-cell} ipython3
# maintenant on nettoie un peu

# convert 201 as int
s = pd.to_numeric(s)
```

```{code-cell} ipython3
s
```

## nettoyer l'index

```{code-cell} ipython3
# stack() a ajouté un niveau artificiel dans le (multi)-index
# niveau 0: en fait la ville
# niveau 1: le numéro de borne dans la ville

# on pourrait faire ceci
# s.index = s.index.droplevel(1)

# mais bien souvent vous trouverez ceci
# comme dans les listes, -1 signifie le dernier niveau

s.index = s.index.droplevel(-1)
```

```{code-cell} ipython3
s
```

## joindre

```{code-cell} ipython3
# pour recoller les deux morceaux
# (*) la dataframe #1 de départ
# (*) cette nouvelle série on va faire un join
# mais pour que ça marche il faut que la série ait un nom
try:
    df1.join(s)
except Exception as exc:
    print(f"{type(exc)}, {exc}")
```

```{code-cell} ipython3
# ce nom se retrouvera dans un nom de colonne du résultat du join()

s.name = 'borne'

df4 = df1.join(s)
```

```{code-cell} ipython3
df4
```

## encore joindre

```{code-cell} ipython3
# et maintenant ya plus qu'à faire le join avec les autres tables pour obtenir les noms 
```

```{code-cell} ipython3
df42 = pd.merge(df4, df2)
df42
```

```{code-cell} ipython3
df423 = df42.merge(df3)
df423
```

## nettoyer

```{code-cell} ipython3
# maintenant on peut se débarrasser des colonnes inutiles

# plusieurs façons

del df423['op_id']
df423
```

```{code-cell} ipython3
# ou encore 
df_final = df423[['ville', 'borne', 'op_name']]
```

```{code-cell} ipython3
df_final
```
