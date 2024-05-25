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
  title: éclater des cellules en colonnes
---

```{code-cell} ipython3
import pandas as pd
```

# groupements

+++

on a fait un sondage, on a demandé à des gens ce qu'ils pensaient devoir être amélioré dans leur environnement

les réponses se présentent comme cela, chaque ligne correspond à une réponse

```{code-cell} ipython3
:cell_style: split

df = pd.read_csv(
    'data/split-count-clean.csv', sep=';')
df
```

+++ {"cell_style": "split"}

on veut faire une synthèse, et pour cela on voudrait transformer ça pour en faire ceci

| city | bins | flowers | toilets | home | answers |
|------|------|---------|---------|------|---------|
| aberdeen | 1 | 3      | 2       | 1    | 3 |
|...|
| london | 1 | 2 | 1 | 0 | 2 |

par exemple pour pouvoir les dessiner simplement

remarquez la colonne `answers` qui décompte le nombre total de réponses dans cette ville

on suppose pour commencer que toutes les réponses sont "propres" c'est-à-dire que toutes les réponses qui parlent de fleurs sont orthographiées de la même façon

+++

## groupement

+++

il faut donc grouper les lignes par ville, et faire une sorte de somme sur les sous-groupes

+++

## idée #1

```{code-cell} ipython3
groups = df.groupby(by='city')
```

```{code-cell} ipython3
groups.aggregate(sum)
```

mais ça c'est pas terrible parce qu'on a des chaines et qu'on va avoir du mal à compter; et aussi vous remarquez le `flowersbathroom` parce qu'on a additionné les chaines brutalement..

donc ce serait mieux de penser en termes de liste

+++

## idée #2

+++

avant de faire la somme, on éclate les chaines en utilisant le séparateur ','

+++

comment on fait ça ? c'est le propos de la méthode `str.split()` 

et rappelez vous, `.str` est utile lorsqu'on veut appliquer une méthode de chaine sur une `df`

```{code-cell} ipython3
df2 = df.copy()
df2['to-improve'] = (
    df2['to-improve']
        .str.replace(' ','')  # ça ne fait pas de mal de nettoyer
        .str.split(',')
)
df2
```

```{code-cell} ipython3
# maintenant je peux faire la somme entre ces listes

totals = df2.groupby('city').aggregate(sum)
totals
```

ça progresse...

+++

## faire le compte

+++

pour faire le compte sur chaque liste, il y a en Python de base une classe Counter

https://docs.python.org/3/library/collections.html#collections.Counter

```{code-cell} ipython3
from collections import Counter
```

c'est peut-être un peu inhabituel  pour les gens qui ne pratiquent pas Python, mais
comme c'est **une classe**, on peut **l'appeler** pour construire un objet - de type `Counter` donc

```{code-cell} ipython3
# un exemple d'appel de Counter sur une liste
Counter(['john', 'mary', 'mary', 'john', 'john', 'john', 'mary'])
```

```{code-cell} ipython3
# je peux donc utiliser apply
# sur la série 'to-improve'
# pour calculer une nouvelle série
# dont les éléments sont des objets 'Counter'
totals['to-improve'].apply(Counter)
```

```{code-cell} ipython3
# et pour l'insérer dans la dataframe, à la place de la précédente
totals['to-improve'] = totals['to-improve'].apply(Counter)

totals
```

## digression

```{code-cell} ipython3
# il faut savoir qu'un objet Counter est aussi un dictionnaire
c = Counter(['john', 'mary', 'mary', 'john', 'john', 'john', 'mary'])
isinstance(c, dict)
```

```{code-cell} ipython3
# on peut donc créer une Series à partir d'un Counter
pd.Series(c)
```

## éclater

+++

Maintenant ce qu'on va faire c'est en gros éclater chaque cellule de droite en ... une nouvelle Series

et là c'est un peu magique il faut bien avouer

1. d'abord la création de la `Series` à partir de `Counter`; qui fait exactement ce qu'on veut, les clés dans l'objet `Counter` servent à remplir l'index de la `Series` 
1. ensuite en remplaçant chaque valeur dans la Series par une nouvelle `Series`, on crée .. une dataframe

```{code-cell} ipython3
# pour bien voir le point #1:
pd.Series(Counter([True, False, False, True, True, True, False]))
```

```{code-cell} ipython3
# et maintenant grâce au point 2, on obtient .. ce qu'on voulait
improvements = totals['to-improve'].apply(pd.Series)

improvements
```

## enfin presque

+++

à ce stade, il nous reste à faire:

1. compter le nombre de réponses (la colonne `answers`)
2. remplacer les n/a par zéro
3. enfin si on regarde attentivement, il y a une colonne en trop, avec un nom vide

  c'est lié à la ligne #4 dans la df de départ, la chaine se termine par une `,`

  du coup quand on fait le `split()` ça nous ajoute une chaine vide, parce que:

```{code-cell} ipython3
# remarquez la chaine vide à la fin du résultat
"a,b,c,".split(',')
```

## le nombre de réponses

```{code-cell} ipython3
answers = df.groupby(by='city').aggregate('count')

complete = improvements.join(answers)
complete
```

```{code-cell} ipython3
# en option on peut renommer la colonne 'to-improve'
complete = complete.rename(columns={'to-improve': 'answers'})
complete
```

## fillna

```{code-cell} ipython3
# on en profite pour remettre des entiers ...
complete.fillna(value=0, inplace=True, downcast='infer')
complete
```

## la colonne 'chaine vide'

+++

on aurait pu traiter le problème à un stade plus précoce, mais à ce stade-ci on peut toujours simplement enlever la colonne

```{code-cell} ipython3
del complete['']
complete
```

## dessiner

```{code-cell} ipython3
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
%matplotlib ipympl
```

```{code-cell} ipython3
complete.plot();
```

```{code-cell} ipython3
complete.T.plot();
```

# v2

+++

pour les rapides, à titre d'exercice:

en vrai les données ne sont pas propres, les gens ont utilisé des synonymes

```{code-cell} ipython3
df = pd.read_csv('data/split-count.csv', sep=';')
df
```

pour essayer de gérer la diversité on se définit - à la main - un tableau de synonymes

```{code-cell} ipython3
synonyms = {
  'bins': ['bin', 'trash', 'dump'],
  'toilets': ['toilet', 'bathroom', 'restroom'],
}
```

et on va utiliser ça pour dire que, par exemple tous les mots qui contiennent "bathroom" ou "restroom" ou "toilet" seront comptabilisés dans la colonne "toilets"

```{code-cell} ipython3
# à vous de jouer...
```

***
