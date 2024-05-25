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
  title: stack() multi-colonnes
---

```{code-cell} ipython3
import pandas as pd
```

# `stack()` en usage un peu plus avancé

```{code-cell} ipython3
df = pd.read_csv("data/stack-multicol.csv")
df
```

c'est donc une version un peut plus évoluée que dans un exercice précédent (`stack-simple`): chaque type est décrit par 3 colonnes

+++

on voudrait le transformer en ceci

| index | city | postcode | type| attribute | value |
|-------|------|----------|------|-----------|--------|
|0|London|90000|t1|nb|1|
|0|London|90000|t1|price|1000|
|0|London|90000|t2|nb|2|
|0|London|90000|t2|price|2000|
|0|Paris|75000|t2|nb|2|
|0|Paris|75000|t2|price|4000|

+++

parce que

* on a enlevé tout ce qui concernait les nb==0
* on ne se donne pas de spécification précise sur l'index, d'où les 0 mais ça peut être ce qu'on veut

```{code-cell} ipython3
types = ['t1', 't2', 't3']
attributes = ['nb', 'price', 'junk']
```

-----

+++

## on coupe en deux

+++

comme dans le premier exercice, on commence par calculer les colonnes qui contiennent les données à retravailler

+++

### les colonnes de la partie droite

+++

on calcule la liste 
`[ "t1_nb", "t1_price", ...]`
à partir du produit cartésien des deux listes

quelque chose comme
```python
for typ in types:
    for attribute in attributes:
        columns.append(f"{typ}_{attribute}")
```

```{code-cell} ipython3
# à vous
true_columns = ...
```

```{code-cell} ipython3
# et maintenant on extrait ces colonnes-là dans une dataframe
df2 = ...
```

### la partie gauche

```{code-cell} ipython3
# il s'agit maintenant de prendre les autres données

# à vous
df_left = ...
```

```{code-cell} ipython3
:cell_style: split

# pour vérification

df_left
```

```{code-cell} ipython3
:cell_style: split

# pour vérification

df2
```

## on crée un MultiIndex

+++

c'est le multi index qui va nous permettre de stacker correctement

**[indice]** `pd.MultiIndex.from_product()`

```{code-cell} ipython3
# fabriquez un multi-index

multi_index = ...
```

```{code-cell} ipython3
# adoptez ce multi-index comme index des colonnes

...
```

```{code-cell} ipython3
# vérifiez visuellement que l'indexation est correcte
df
```

```{code-cell} ipython3
df2
```

## on nettoie (1): `junk`

+++

rappelez-vous qu'on ne s'intéressait pas aux données `junk`  
du coup il est temps de nettoyer la table de ces colonnes-là

**[note]** ceux qui suivent vont trouver une façon de faire qui implique de remonter dans le temps  
c'est vrai qu'on aurait pu faire comme ça, mais essayez tout de même de trouver une façon de le faire maintenant

```{code-cell} ipython3
# à vous pour le nettoyage
...
```

## `stack()`

+++

à ce stade tout est prêt quasiment pour actionner la magie de `stack()`, essayez et regardez ce que ça vous donne

```{code-cell} ipython3
# à vous

df3 = ...
```

```{code-cell} ipython3
:cell_style: split

df2
```

```{code-cell} ipython3
:cell_style: split

df3
```

## on nettoie (2): les colonnes vides

+++

ça n'était'était pas vraiment exprès au départ
mais c'est intéressant: aucune ville n'a de t3

```{code-cell} ipython3
# à vous de supprimer les colonnes sans intérêt
...
```

## `stack()` à nouveau

+++

maintenant qu'on s'est débarrassés de `t3`, 
on peut stacker à nouveau
comme on avait fait dans `stack-simple`

et comme dans `stack-simple` on obtient une série car l'index des colonnes est simple

```{code-cell} ipython3
# à vous

s = ...
```

## les labels

+++

en première lecture, passez cette question, puis quand vous arriverez à la fin revenez-y pour affiner les labels dans le résultat final

```{code-cell} ipython3
# laissez vide en première lecture
```

```{code-cell} ipython3
s
```

## etc...

+++

essentiellement maintenant, c'est la même logique que dans `stack-simple`, je vous laisse finir

**[indices]** `reset_index()` et `join()`

```{code-cell} ipython3
# à vous

df_right = ...
```

```{code-cell} ipython3
# à vous

df_final = ...
```

```{code-cell} ipython3
df_final
```

****

+++

## pas demandé

```{code-cell} ipython3
:tags: [raises-exception]

# ce n'était pas demandé, mais 
# si on veut remettre un index propre, on n'a qu'à faire
df_final.index = pd.RangeIndex(0, len(df_final))
df_final
```

## à quoi ça sert

```{code-cell} ipython3
:tags: [raises-exception]

# en tous cas, sous cette forme, on peut s'intéresser à un type particulier
df_t1 = df_final.loc[df_final.attribute == 't1', :]
df_t1
```

```{code-cell} ipython3
:tags: [raises-exception]

# ou juste les nombres
df_t1_nb = df_t1[df_t1.type == 'nb']
df_t1_nb
```
