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
  title: stack() multi-colonnes
---

# `stack()`: usage un peu plus avancé

```{code-cell} ipython3
import pandas as pd
```

ceci est une version un peu plus évoluée que dans l'exercice précédent [](#label-exo-stack-simple)  
sauf que cette fois-ci, chaque type (t1, t2, t3, ...) est décrit par 3 colonnes

```{code-cell} ipython3
df = pd.read_csv("data/stack-multicol.csv")
df
```

et notre objectif est de le transformer en ceci

```{div}
:label: exo-stack-multicol-target

| index | city | postcode | type| attribute | value |
|-------|------|----------|------|-----------|--------|
|0|London|90000|t1|nb|1|
|0|London|90000|t1|price|1000|
|0|London|90000|t2|nb|2|
|0|London|90000|t2|price|2000|
|0|Paris|75000|t2|nb|2|
|0|Paris|75000|t2|price|4000|
```

+++

notez bien que

* on a enlevé tout ce qui concernait les nb==0
* on ne se donne pas de spécification précise sur l'index, d'où les 0 mais ça peut être ce qu'on veut

```{code-cell} ipython3
# quelques variables utiles pour la suite

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

````{admonition} indice
:class: dropdown tip

quelque chose comme
```python
for typ in types:
    for attribute in attributes:
        columns.append(f"{typ}_{attribute}")
```
````

```{code-cell} ipython3
# à vous
true_columns = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# ce qui donne en version Pythonique
# notez qu'on pourrait aussi bien utiliser itertools.product

true_columns = [
    f"{typ}_{attribute}"
    for typ in types for attribute in attributes
]
```

```{code-cell} ipython3
# et maintenant on extrait ces colonnes-là dans une dataframe
df2 = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# j'extrais les colonnes qu'il va falloir tripoter
df2 = df[true_columns]
```

### la partie gauche

```{code-cell} ipython3
# il s'agit maintenant de prendre les autres données
# i.e. les colonnes qui ne sont pas dans df2

# à vous
df_left = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# et à gauche je garde juste les autres colonnes
# je fais une copie surtout pour que le notebook soit idempotent

df_left =  df.copy()

# no longer need these
for column in true_columns:
    del df_left[column]
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# on pourrait aussi faire comme ceci
left_columns = list(set(df.columns) - set(true_columns))
df_left = df[left_columns]
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

```{admonition} indice
:class: dropdown tip

voyez `pd.MultiIndex.from_product()`
```

```{code-cell} ipython3
# fabriquez un multi-index

multi_index = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# c'est important de les mettre dans cet ordre
# parce que c'est dans cet ordre que sont les données d'entrée
multi_index = pd.MultiIndex.from_product([types, attributes])
```

```{code-cell} ipython3
# adoptez ce multi-index comme index des colonnes de df2

...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# c'est ici que se passe le truc important
# parce qu'on commence à lier les données en groupes
df2.columns = multi_index
```

```{code-cell} ipython3
# vérifiez visuellement que les colonnes sont indexées correctement


df2
```

## on nettoie (1): `junk`

+++

rappelez-vous qu'on ne s'intéressait pas aux données `junk`  
du coup il est temps de nettoyer la table de ces colonnes-là

```{admonition} note - on aurait pu le faire plus tôt
:class: dropdown note

ceux qui suivent vont trouver une façon de faire qui implique de remonter dans le temps  
(je veux dire de traiter ce point plus tôt dans le notebook)  
c'est vrai qu'on aurait pu faire comme ça, mais essayez tout de même de trouver une façon de le faire maintenant
```

```{code-cell} ipython3
# à vous pour le nettoyage
...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell
# la remontée dans le temps consiste tout simplement à ne pas mentionner
# 'junk' dans la variable `attributes` au début du notebook
# mais alors on aurait retrouvé ces données dans df_left,
# qu'il faudrait alors calculer autrement...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# en utilisant l'indexation dans les multi-index c'est relativement facile

# on nettoie la donnée qui ne nous intéressait pas
for typ in types:
    del df2[(typ, 'junk')]
df2
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# je ne me suis pas hasardé à essayer avec un slice, ça semble un truc qui
# doit pouvoir se faire
```

## `stack()`

+++

à ce stade tout est prêt quasiment pour actionner la magie de `stack()`, essayez et regardez ce que ça vous donne

```{code-cell} ipython3
# à vous

df3 = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# ici l'appel à stack() nous donne une dataframe
# à cause du multi-index dans la attribute des colonnes
df3 = df2.stack()
type(df3), df3
```

```{code-cell} ipython3
:cell_style: split

# pour vérifier

df2
```

```{code-cell} ipython3
:cell_style: split

# pour vérifier

df3
```

## on nettoie (2): les colonnes vides

+++

ça n'était pas vraiment délibéré au départ  
mais le cas est intéressant: aucune ville n'a de t3

```{code-cell} ipython3
# à vous de supprimer les colonnes sans intérêt
...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# on supprime les colonnes inutiles
df3 = df3.loc[:, df3.sum()>0]
df3
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

```{code-cell} ipython3
:cell_style: center
:tags: [level_basic]

# prune-cell

s = df3.stack()
s
```

## les labels

+++

en première lecture, passez cette question, puis quand vous arriverez à la fin revenez-y pour affiner les labels dans le résultat final

```{code-cell} ipython3
# laissez vide en première lecture
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# ce sera le nom de la dernière colonne dans le résultat final

s.name = 'value'
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

# on met les noms qui vont bien dans le multi-index (des lignes)

s.index.names = [None, 'attribute', 'type']
```

```{code-cell} ipython3
s
```

## etc...

+++

essentiellement maintenant, c'est la même logique que dans l'exercice [](#label-exo-stack-simple), je vous laisse finir [pour obtenir le résultat souhaité](#exo-stack-multicol-target)

```{admonition} indice
:class: dropdown tip

voir `reset_index()` et `join()`
```

```{code-cell} ipython3
# à vous

df_final = ...
```

```{code-cell} ipython3
:cell_style: center
:tags: [level_basic]

# prune-cell

# on transforme les deux étages de l'index (des lignes)
# en colonnes 'normales'

df_right = s.reset_index(level=(1, 2))
type(df_right), df_right
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell 

# du coup maintenant on n'a plus qu'à joindre les deux
df_final = df_left.join(df_right)
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

## à quoi ça sert ?

les usages pour ce type de traitement sont nombreux, par exemple

```{code-cell} ipython3
:tags: [raises-exception]

# sous cette forme, on peut s'intéresser à un type particulier

df_t1 = df_final.loc[df_final.type == 't1', :]
df_t1
```

```{code-cell} ipython3
:tags: [raises-exception]

# ou juste les nombres

df_t1_nb = df_t1[df_t1.attribute == 'nb']
df_t1_nb
```
