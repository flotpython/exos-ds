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
---

# dessins par groupby

et accessoirement, lire plusieurs feuillets depuis excel

{download}`mais commencez par télécharger le zip<./ARTEFACTS-groupby-draw.zip>`

+++

le fichier excel `data/groupby-draw.xlsx` contient ici plusieurs feuillets

+++

```{image} media/groupby-draw-excel.png
:align: center
```

+++

les deux feuillets contiennent 2 données différentes pour les mêmes sites / dates

+++

## ce qu'il faut faire

+++

A. visualiser les deux données (Sessions et Waiters) en fonction du temps par site

e.g.

<img src="media/groupby-draw-sessions.png" width=600px>

+++

B. mêmes chiffres mais agrégés sur les sites, les deux caratéristiques sur une seule figure (ici avec seaborn)

<img src="media/groupby-draw-both.png" width=600px>

```{code-cell} ipython3
# à vous

# imports ...
```

```{code-cell} ipython3
df = ...
```

---

```{code-cell} ipython3
# prune-begin
import pandas as pd
import matplotlib.pyplot as plt
```

```{code-cell} ipython3
import seaborn as sns
```

```{code-cell} ipython3
plt.rcParams["figure.figsize"] = (12, 4)
plt.style.use('seaborn')
sns.set(rc={'figure.figsize': (12, 4)})
```

## lire

```{code-cell} ipython3
dfs = pd.read_excel("data/groupby-draw.xlsx", sheet_name=None)
```

```{code-cell} ipython3
# ATTENTION avec sheet_name=None
# le résultat de read_excel N'EST PAS une dataframe
type(dfs)
```

```{code-cell} ipython3
list(dfs.keys())
```

```{code-cell} ipython3
df1, df2 = dfs['Sessions'], dfs['Waiters']
df2.head(3)
```

```{code-cell} ipython3
len(df1), len(df2)
```

```{code-cell} ipython3
df1['Site Name'].unique()
```

## merger

+++

on peut merger comme ça brutalement et ça fonctionne

```{code-cell} ipython3
# m pour merged

m = pd.merge(df1, df2)
len(m)
```

```{code-cell} ipython3
# mais il est toujours recommandé de bien spécifier 
# comment doit se faire le merge
```

```{code-cell} ipython3
m = pd.merge(df1, df2, left_on=['Date', 'Site Name'], right_on=['Date', 'Site Name'])
```

```{code-cell} ipython3
m.head(2)
```

```{code-cell} ipython3
# et là à ce stade on peut - pas du tout obligatoire - 
# dropper les deux colonnes qui on été dupliquées du coup
del m['Property Type_x']
del m['Property Type_y']
```

```{code-cell} ipython3
m.head(2)
```

## tracé (1)

```{code-cell} ipython3
# ouh là, ça fait mal à la tête 
# l'explication est plus bas, on va décortiquer ça ... :)

m.groupby(by=['Date', 'Site Name'])['Sessions'].sum().unstack().plot();
```

### décortiquons un peu

```{code-cell} ipython3
# on commence par faire un groupby sur la date et le site
# j'itère dessus mais c'est juste pour comprendre ce qu'il y a dedans

i = 0
for crit, subdf in m.groupby(by=['Date', 'Site Name']):
    print(crit, '->', subdf)
    i += 1
    if i == 3:
        print('...')
        break
```

```{code-cell} ipython3
# de là on peut extraire une colonne
# du coup sur le groupby['colonne'] on peut itérer sur des sous-series
# et non plus des sous-dataframes

i = 0
for crit, subseries in m.groupby(by=['Date', 'Site Name'])['Sessions']:
    print(crit, '->', subseries)
    i += 1
    if i == 3:
        print('...')
        break
```

```{code-cell} ipython3
# en appliquant sum() on transforme le groupby de series .. en une dataframe !
# à chaque fois ici `sum()` fait la somme de un seul nombre
# c'est juste pour changer le type du résultat
m.groupby(by=['Date', 'Site Name'])['Sessions'].sum()
```

```{code-cell} ipython3
# du coup à la fin grâce à un subtil unstack(), on a exactement
# ce qu'on veut, qu'on va pouvoir tracer tel quel en fait

m.groupby(by=['Date', 'Site Name'])['Sessions'].sum().unstack()
```

```{code-cell} ipython3
import matplotlib.pyplot as plt

# avec quelques décorations pour faire joli
m.groupby(by=['Date', 'Site Name'])['Sessions'].sum().unstack().plot(
    figsize=(12, 8),
    xlabel='date',
    ylabel='sessions',
    title='sessions\nover the summer',
);
plt.savefig(fname='media/groupby-draw-sessions.png')
```

```{code-cell} ipython3
# avec quelques décorations pour faire joli
m.groupby(by=['Date', 'Site Name'])['Waiters'].sum().unstack().plot(
    figsize=(12, 8),
    xlabel='date',
    ylabel='waiters',
    title='waiters\nover the summer',
);
plt.savefig(fname='media/groupby-draw-waiters.png')
```

## tracé (2)

+++

le plus gros du travail consiste à mettre les données sous la bonne forme

* un multi-index sur les colonnes
* une ligne par date

```{code-cell} ipython3
m2 = m.groupby(by=['Date', 'Site Name'])[['Sessions', 'Waiters']].sum().unstack()
m2
```

```{code-cell} ipython3
import seaborn as sns

sns.relplot(data=m2, kind='line')
plt.savefig("media/groupby-draw-both.png")
```

### idem avec pivot_table

```{code-cell} ipython3
# la même chose avec un pivot_table
m3 = m.pivot_table(values=['Sessions', 'Waiters'], index='Date', columns='Site Name')
```

```{code-cell} ipython3
sns.relplot(data=m3, kind='line');
```
