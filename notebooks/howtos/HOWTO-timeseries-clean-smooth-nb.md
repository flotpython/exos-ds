---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
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
  title: "des timeseries r\xE9alistes"
---

<div class="licence">
<span>Licence CC BY-NC-ND</span>
<span>Thierry Parmentelat</span>
</div>

+++

# time series

+++

partons d'un jeu de données réel qui décrit des grandeurs géophysiques sur une période plus de 10 ans avec une fréquence de 1h

```{code-cell} ipython3
import pandas as pd
```

## `pd.read_excel`

+++

ce qui va nous donner une occasion de travailler sur un fichier `.xlsx`  

pour cela le point d'entrée c'est `pd.read_excel`, mais il faut savoir que cela demande une dépendance supplémentaire

```{code-cell} ipython3
# il se peut que cette cellule vous dise 
# Missing optional dependency 'openpyxl'

try:
    df = pd.read_excel("data/DB_Galion.xlsx")
except Exception as exc:
    print(f"OOPS {type(exc)} {exc=}")
```

du coup si nécessaire, faites l'installation de `openpyxl` comme indiqué, par exemple:

```{code-cell} ipython3
%pip install openpyxl
```

## chargement

```{code-cell} ipython3
# c'est un peu long - sans doute à cause du format des dates
# aussi on va ranger ça dans un coin 
# et si nécessaire, on copiera ça au lieu de recharger
df_original = pd.read_excel("data/DB_Galion.xlsx")
```

```{code-cell} ipython3
# repartir d'ici si on a besoin de repartir de 0:
df = df_original.copy()
df.head()
```

pour info, les données en question signifient ceci:

| colonne | nom complet |
|-|-|
| NP | Niveau Puits |
| PA | Pression Atmosphérique |
| MG | Marée Océanique (Marée Géographique) |
| ET | Marée terrestre (Earth Tide) |

```{code-cell} ipython3
# quelques ordres de grandeur
df.info()
```

ça fait tout de même 120.000 entrées de 4 mesures chacune; ça ne va pas être possible de faire une inspection visuelle de tout ça

voyons un peu le genre de chose qu'on peut faire automtiquement pour s'assurer de la complétude / cohérence de ces données

+++

## index

+++

pour commencer, le plus urgent est presque toujours de transformer les données temporelles dans un type pertinent;  
ici par chance (grâce à `read_excel` qui est intelligent) la colonne de temps est **déjà** dans le bon type, comme on le voit ci-dessus dans le résultat de `df.info()`

+++

ici comme souvent, on va choisir cette colonne comme index, c'est vraiment naturel

```{code-cell} ipython3
df = df.set_index('Date_Heure_locale')
df.head(2)
```

## aperçu

+++

notre objectif: passer le moins de temps possible pour voir une vague idée de ces données

```{code-cell} ipython3
# version simplissime: vraiment pas top
df.plot();
```

la première amélioration vient au prix d'une ligne qu'on mentionne généralement au début (autour de par exemple la ligne `import pandas as pd`)

+++

### `%matplotlib ipympl`

```{code-cell} ipython3
%matplotlib ipympl
```

```{code-cell} ipython3
# une fois qu'on a choisi ce mode on obtient des visus interactives
# on peut agrandir la figure, zoomer, se déplacer, etc...
df.plot();
```

### `figsize`

+++

si vous voulez choisir une taille par défaut pour les figures

```{code-cell} ipython3
# il y a plein d'options pour faire ça
# j'aime bien celle-ci, mais bon...

from IPython.core.pylabtools import figsize
figsize(8, 6)
```

```{code-cell} ipython3
# et à partir de là...
df.plot();
```

```{code-cell} ipython3
# sachant qu'on peut toujours choisir la taille
# pour une figure donnée
df.plot(figsize=(3, 3));
```

### `subplots=True`

+++

comme les échelles ne sont pas forcément les mêmes, ou pour plein d'autres raisons, on peut avoir envie de voir les données indépendamment les unes des autres

```{code-cell} ipython3
df.plot(subplots=True);
```

## il manque une colonne !

+++

on n'y voit toujours pas grand-chose, et surtout **il nous manque une colonne**  
vous l'avez peut-être remarqué tout à l'heure, mais la colonne `NP` n'est pas sortie correctement du `read_excel` car

```{code-cell} ipython3
df.dtypes
```

pour bien trouver tous les soucis avec cette colonne:

```{code-cell} ipython3
# voyons ce que donne pd.to_numeric

try:
    pd.to_numeric(df.NP)
except Exception as exc:
    print(f"OOPS {type(exc)} {exc=}")
```

ce qui nous indique qu'il y a au moins un endroit où la colonne NP contient une chaine composée d'un espace; voyons combien il y en a de ce genre

```{code-cell} ipython3
(df.NP == ' ').value_counts()
```

fort heureusement on peut forcer la conversion comme ceci

```{code-cell} ipython3
pd.to_numeric(df.NP, errors='coerce')
```

cette fois la conversion se fait correctement; il ne faut pas oublier par contre de bien **adopter** la nouvelle colonne - car avec la cellule précédente on a calculé un nouvelle colonne mais elle ne fait pas partie de la dataframe

```{code-cell} ipython3
# comme on est satisfait on remplace la colonne dans la dataframe
df['NP'] = pd.to_numeric(df.NP, errors='coerce')
```

```{code-cell} ipython3
# et du coup maintenant on a bien des nombres partout
df.dtypes
```

## aperçu (2)

+++

reprenons maintenant notre aperçu

```{code-cell} ipython3
:scrolled: false

df.plot(subplots=True);
```

### `alpha=0.1`

+++

si on insiste pour voir les 4 données dans la même vue, comme on avait fait pour commencer, il y a tellement de données en X qu'on ne voit que la dernière colonne !

dans ces cas-là le canal alpha (la transparence) est notre meilleur allié

```{code-cell} ipython3
df.plot(alpha=0.1);
```

## changement d'échelle

+++

où on voit que nous avons surtout un problème avec les échelles, car `ET` - qui est en principe du même ordre de grandeur que `MG` - a beaucoup plus d'amplitude

+++

ce qui nous donne l'occasion de faire des statistiques basiques

```{code-cell} ipython3
:cell_style: split

df.MG.describe()
```

```{code-cell} ipython3
:cell_style: split

df.ET.describe()
```

comme je n'en sais pas plus sur ces données, je vais arbitrairement diviser `ET` par 1000

```{code-cell} ipython3
df['ET'] /= 1000
```

## nan ?

+++

à ce stade on a donc des nan - au moins dans NP, ça on en est sûr, et dans les autres colonnes peut-être aussi

```{code-cell} ipython3
# dans une colonne en particulier
df.NP.isna().sum()
```

```{code-cell} ipython3
# si on veut une information plus globale, par exemple
df.isna().sum(axis=0)
```

### comment sont-ils répartis ?

+++

ce qu'on aimerait savoir maintenant, c'est est-ce que les 'trous' sont plutôt éparpillés ou plutôt groupés; et pour ça on va

* fabriquer une série qui contient les timestamps où on a une mesure (en enlevant ceux qui correspondent à un nan, donc)
* puis on fera la différence avec la valeur immédiatement voisine (pour cela on décale les valeurs de 1 cran, et on fait la différence)

```{code-cell} ipython3
# par exemple avec la colonne NP qui a les plus beaux trous
NP = df.NP.copy()

# on isole les lignes qui ont une valeur
NP_defined = NP[NP.notna()]

# ce qui nous intéresse ce sont les timestamps
NP_times = NP_defined.index

# combien de mesures en tout, combien de mesures pertinentes
NP.shape, NP_times.shape
```

```{code-cell} ipython3
# la grosse astuce consiste à mettre les timestamps comme valeurs
# et pour ça on utilise la fonction pd.to_series 
# souvenez-vous que NP_times est un objet Index

NP_times_series = NP_times.to_series()
NP_times_series
```

```{code-cell} ipython3
# et du coup maintenant on peut décaler (avec shift()) les valeurs de 1 cran

NP_times_series.shift()
```

```{code-cell} ipython3
# et surtout faire la différence entre les deux, qui normalement doit donner 1h

D = NP_times_series - NP_times_series.shift()
```

```{code-cell} ipython3
# si on voulait enlever une heure justement, on ferait

D = NP_times_series - NP_times_series.shift() - pd.to_timedelta("01:00:00")
D.head()
```

```{code-cell} ipython3
from datetime import timedelta as TimeDelta

TimeDelta()
```

```{code-cell} ipython3
# du coup pour isoler juste les trous on ferait
D_holes = D[~(D==TimeDelta())]
D_holes.shape
```

```{code-cell} ipython3
D_holes = D_holes.sort_values(ascending=False)
D_holes
```

### de drôles de trous

+++

le début de la table est intéressant, mais à la fin ... on trouve des trous de -1h !

et comme nous avions artificiellement retiré une heure, ça signifie qu'en fait on a des doublons !

```{code-cell} ipython3
doublons = D_holes[D_holes == TimeDelta(hours=-1)]
```

```{code-cell} ipython3
doublons.shape
```

```{code-cell} ipython3
doublons
```

```{code-cell} ipython3
# pour une inspection visuelle
df.loc[doublons.index]
```

```{code-cell} ipython3
real_holes = doublons = D_holes[D_holes != TimeDelta(hours=-1)]
```

```{code-cell} ipython3
print(f"nous avons trouvé {len(real_holes)} trous dans la colonne NP")
real_holes
```

```{code-cell} ipython3
# si on veut les montrer
# c'est mieux de transformer en heures (sinon on a des nano-secondes apparemment)
# en plus comme on n'a pas une dataframe, avec le driver %matlotlib notebook
# il faut créer une nouvelle figure

import matplotlib.pyplot as plt

plt.figure()
(real_holes / TimeDelta(hours=1)).plot(style=['r']);
```

## un peu de lissage

+++

on regarde cette fois la courbe 'PA'; utilisez le zoom pour regarder environ un mois

```{code-cell} ipython3
plt.figure()
PA = df.PA
PA.plot();
```

on voit que la fluctuation en tendance est obscurcie par des variations de plus haute fréquence; on va essayer de lisser ce signal pour ne conserver que la tendance de fond

normalement sur ce zoom vous devriez percevoir que la haute fréquence est de l'ordre de la demie journée

```{code-cell} ipython3
plt.figure()
PA.plot()
PA.rolling(24, center=True).mean().plot(style=['r']);
PA.rolling(12, center=True).mean().plot(style=['g']);
```

***
