---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
language_info:
  name: python
  pygments_lexer: ipython3
  nbconvert_exporter: python
nbhosting:
  title: stack() simple
---

(label-exo-stack-simple)=
# `stack()`: usage typique

```{code-cell} ipython3
import pandas as pd
```

on a des données qui ressemblent à ceci

```{code-cell} ipython3
df = pd.read_csv("data/stack-simple.csv")
df
```

on veut produire une table simplifiée qui ressemblerait à ceci; on élimine les lignes qui correspondraient à une valeur nulle

|city|postcode|type|nombre| 
|-|-|-|-|
| London | 90000 | t1 | 1 |
| London | 90000 | t2 | 2 |
| London | 90000 | t3 | 3 |
| Paris  | 75000 | t2 | 4 |
| Paris  | 75000 | t3 | 2 |
| Paris  | 75000 | t4 | 3 |

+++

---

+++

## se concentrer sur les colonnes ti

```{code-cell} ipython3
# commencez par extraire les colonnes spéciales
columns = ['t1', 't2', 't3', 't4']

df2 = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

df2 = df[columns]
df2
```

## `stack()`

+++

**attention** comme on a un **index simple** sur les colonnes, le `stack()` nous produit **une Series**

```{code-cell} ipython3
# appliquez un simple `stack()` sur la dataframe df2
# regardez le contenu et le type

series = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

series = df2.stack()

# ici on obtient une série
series = df2.stack()
series
```

## on peut nettoyer les 0

+++

on peut se passer de cette étape si on a des n/a à la place des 0; mais ici, c'est le moment de nettoyer

```{code-cell} ipython3
# à vous
...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

series = series[series != 0]
series
```

## passer de l'index à une colonne 'usuelle'

+++

maintenant, que faut-il faire avec la donnée `type` pour se rapprocher de ce qu'on cherche à produire ?

```{admonition} indice
:class: dropdown tip
voyez `df.reset_index()`
```

```{code-cell} ipython3
# à vous

df3 = ...
```

+++ {"tags": ["level_basic"]}

prune-cell

on promeut le deuxième niveau de l'index (level==1) comme une colonne normale

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# ici on transforme la pseudo-colonne index de niveau 2
# on pourrait aussi mettre level=1, c'est le niveau le + profond

df3 = series.reset_index(level=-1)
df3
```

## nommer

```{code-cell} ipython3
# les noms des colonnes dans df3 ne sont vraiment pas terribles

# à vous...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

# une option qui marche aussi
# df3.columns = ['type', 'nb_bornes']

df3 = df3.rename(columns={'level_1': 'type', 0: 'nb_bornes'})
df3
```

## recoller

+++

à ce stade il ne reste plus qu'à recoller les morceaux

```{admonition} indice
:class: dropdown tip
voyez `pd.merge()` et/ou `df.join()`
```

```{code-cell} ipython3
# à vous

df_all = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

df_all = df.join(df3)
df_all
```

## nettoyer

+++

et enfin, à éliminer les colonnes qui sont de trop

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

for col in df_all.columns:
    if col in columns:
        del df_all[col]
```

```{code-cell} ipython3
# pour vérifier le résultat de visu
# df_all
```

***

+++

## `pd.melt()`

Il se trouve qu'on peut arriver à ce même résultat avec [une fonction toute faite de pandas qui s'appelle `pd.melt()`](https://pandas.pydata.org/docs/reference/api/pandas.melt.html)  
Mais bon, pour bien comprendre la librairie c'est sans doute mieux de passer par des manipulations de base comme on vient de le faire :)

```{code-cell} ipython3
# prune-cell

df = pd.read_csv("data/stack-simple.csv")

df_long = pd.melt(
    df,
    id_vars=['city', 'postcode'],   # columns to keep
    var_name='type',                # new column name for variable names (t1, t2, ...)
    value_name='nombre'             # new column name for values
)

# Optionally, drop rows with zero or missing values
df_long = df_long[df_long['nombre'] != 0].reset_index(drop=True)

print(df_long)
```

***
