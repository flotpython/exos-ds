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
  title: exo titanic
---

# les passagers du titanic

```{code-cell} ipython3
import pandas as pd
```

## les données

```{code-cell} ipython3
df_raw = pd.read_csv('data/titanic.csv', index_col='PassengerId')
```

**remarquez** *que vous pouvez aussi charger les même données via `seaborn`*
```python
import seaborn as sns
ti = sns.load_dataset('titanic')
```

```{code-cell} ipython3
df_raw.head()
```

----

+++

## simplification

+++

**[consigne]** simplifier la table, ne gardez que les colonnes qui après renommage s'appellent `survived`, `class`, `sex`, `age`, et `harbour` (pour `Embarked`)

```{code-cell} ipython3
# à vous
df = ...
```

```{code-cell} ipython3
:tags: [raises-exception]

df.head()
```

## taux de survie par sexe

+++

**[consigne]** calculez le taux de survie par sexe (2 valeurs)

```{code-cell} ipython3
# à vous
...
```

## survie selon deux critères (méthode manuelle)

+++

**[consigne]** calculez le taux de survie par sexe et classe (6 valeurs)

dans un premier temps, on va utiliser `groupby()` et produire une `Series`

+++

en une formule relativement simple, vous pouvez créer à base de `groupby` une série des 6 valeurs représentant le taux de survie du groupe

```{code-cell} ipython3
# à vous
```

## moyenne avec pivot_table()

+++

**[consigne]]** utilisez à présent `pivot_table()` pour produire les mêmes résultats mais dans una table de dimension 2 lignes x 3 colonnes; puis 3 lignes et 2 colonnes

```{code-cell} ipython3
# 2 lignes x 3 colonnes
# à vous
```

```{code-cell} ipython3
# 3 lignes x 2 colonnes
# à vous
```

## nombre de survivants avec pivot_table()

+++

**[consigne]** toujours avec `pivot_table()` produisez dans une table 2x3 le **nombre** de survivants

+++

### double-check

+++

**[consigne]** vérifiez que la somme des nombres dans cette table coincide bien avec le nombre de survivants dans la donnée de départ

+++

## pivot_table multi-colonnes

+++

## afficher le taux de survie et la moyenne d'âge

+++

maintenant on va aussi prendre en compte l'âge

**[consigne]** produisez une table avec 12 valeurs, avec pour chacun des 6 groupes le **taux de survie** et la **moyenne d'âge**  
  visez de présenter les données
  * sur deux lignes (selon le sexe)
  * et sur chaque ligne, 3 valeurs (selon la classe) pour le taux de survie, et 3 valeurs pour la moyenne d'âge

```{code-cell} ipython3
# 2 lignes
# sur chaque ligne, d'abord 3 taux de survie, puis 3 moyennes d'âge

# à vous
...
```

### afficher la moyenne d'âge entre survivants et entre disparus

+++

**[consigne]** on veut produire une table qui a 12 valeurs aussi, mais qui modélise seulement la moyenne d'âge selon les mêmes groupes, et selon que les gens ont survécu ou non

**[attention]** il y a toujours 12 chiffres à afficher, mais bien entendu 
ce ne sont plus les mêmes chiffres que l'on doit obtenir ici

```{code-cell} ipython3
# à vous
...
```

## groupements en *bins*

+++

**[consigne]** on répartit arbitrairement les individus en 5 classes d'âge: les enfants de moins de 10 ans, les adolescents de moins de 20ans, les jeunes adultes de moins de 40 ans, les adultes en dessous de 60 ans, et les seniors au delà.

affichez maintenant le taux de survie selon 10 groupes, liés à 
  * le sexe
  * la classe d'âge

```{code-cell} ipython3
# à vous
```

## pivot sur données catégorielles

+++

**[consigne]** selon toujours les 2 critères `sex` et `class`, indiquez pour chacun des 6 groupes quelle est la classe d'âge majoritaire

**[indice]** `Series.mode()`

```{code-cell} ipython3
# à vous
```
