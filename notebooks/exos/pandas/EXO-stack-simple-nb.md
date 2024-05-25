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
  title: stack() simple
---

# usage typique de `stack()`

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

## `stack()`

+++

**attention** comme on a un **index simple** sur les colonnes, le `stack()` nous produit **une Series**

```{code-cell} ipython3
# appliquez un simple `stack()` sur la dataframe df2
# regardez le contenu et le type

series = ...
```

## on peut nettoyer les 0

+++

on peut se passer de cette étape si on a des n/a à la place des 0; mais ici, c'est le moment de nettoyer

```{code-cell} ipython3
# à vous
...
```

## passer de l'index à une colonne 'usuelle'

+++

à ce stade, que faut-il faire avec la donnée `type` pour se rapprocher de ce qu'on cherche à produire ?

**[indice]** voyez `df.reset_index()`

```{code-cell} ipython3
# à vous

df3 = ...
```

## nommer

```{code-cell} ipython3
# les noms des colonnes dans df3 ne sont vraiment pas terribles

# à vous...
```

## recoller

+++

à ce stade il ne reste plus qu'à recoller les morceaux

**[indice]** `pd.merge()` et/ou `df.join()`

```{code-cell} ipython3
# à vous
```

## nettoyer

+++

et enfin, à éliminer les colonnes qui sont de trop

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
# pour vérifier le résultat de visu
# df_all
```

***
