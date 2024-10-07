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

# time series: nettoyer et lisser 

pour exécuter ce code localement sur votre ordi, 
{download}`commencez par télécharger le zip<./ARTEFACTS-timeseries-clean-smooth.zip>`

+++

partons d'un jeu de données réel qui décrit des grandeurs géophysiques sur une période plus de 10 ans avec une fréquence de 1h

```{code-cell} ipython3
import pandas as pd
```

## `pd.read_excel`

ce qui va nous donner une occasion de travailler sur un fichier `.xlsx`  
pour cela le point d'entrée c'est `pd.read_excel`, mais il faut savoir que cela demande une dépendance supplémentaire

du coup si nécessaire, faites l'installation de `openpyxl` comme indiqué, par exemple:

```{code-cell} ipython3
# uncomment if needed
# %pip install openpyxl
```

## chargement

le premier chargement "naif" avec `read_excel` nous permet de voir que la donnée temporelle ressemble à ceci
```text
18/08/2006 21:00
```

aussi on va utiliser ce format pour charger "proprement" notre dataframe; cela va avoir deux avantages

- d'abord, on est sûr de notre affaire; on ne risque pas de laisser `read_excel` inventer des dates folkloriques
- ensuite, ça ne peut qu'accélérer le chargement

````{admonition} tip
:class: tip

pour trouver la liste des caractères valides dans un time format, cherchez sur google, par exemple

> python date format characters
````

```{code-cell} ipython3
# c'est un peu long à charger
# aussi on va ranger ça dans un coin 
# et si nécessaire, on copiera ça au lieu de recharger

FORMAT = "%d/%m/%Y %H:%M"

try:
    df_original
    print("using preloaded data")
except NameError:
    df_original = pd.read_excel("data/DB_Galion.xlsx", date_format=FORMAT)
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

voyons un peu le genre de chose qu'on peut faire automatiquement pour s'assurer de la complétude / cohérence de ces données

+++

## préparation

pour commencer, la todo list est souvent celle-ci:

- le plus urgent est presque toujours de transformer les données temporelles dans un type pertinent;  
ici on l'a déjà fait au moment du chargement, comme on le voit ci-dessus dans le résultat de `df.info()`
- avant de choisir un index; s'assurer de l'unicité
- adopter l'index

ici notre colonne candidat pour être l'index, c'est cette colonne temporelle, c'est vraiment naturel

````{admonition} soyons prudent

cette étape est un peu scabreuse, mais je fais bien tout pas à pas pour qu'on soit sûr; 
c'est très important de faire super attention au moment du nettoyage !
````

+++

### unicité ?

```{code-cell} ipython3
:scrolled: true

# pour être propre, on veut s'assurer que la colonne en question
# est bien à valeurs uniques 

# normalement value_counts() ne devrait contenir que des 1
counts = df.Date_Heure_locale.value_counts()
dups = counts[counts != 1]

# en fait on a plusieurs entrées correspondant à ces moments-là:
dups
```

```{code-cell} ipython3
# pour combien de dates a-t-on 2 données

len(dups)
```

```{code-cell} ipython3
# voyons un peu ces multi-entrées

# on ne peut pas encore écrire directement ceci
# car justement on n'a pas encore mis la date en index
#df.loc[dups.index]

# on passe par une df temporaire qui a le bon index
# et on regarde les 3 premiers doublons

df.set_index('Date_Heure_locale').loc[dups.index[:3]]
```

mmh, c'est assez étrange, les 3 premières colonnes ont des données quasi identiques au moment du doublon, mais pas la 4ème...

compte tenu du faible nombre de lignes concernées, on va prendre une décision conservatoire, qui est de garder, pour chacun de ces 13 instants, **la moyenne des deux mesures**

sauf que, si on essaie de faire ça  ce stade, on est confronté au fait que la colonne `NP` est de type `object`...

+++

### une colonne de type `object`

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

### la moyenne

on peut à présent faire la moyenne pour les doublons

```{code-cell} ipython3
df = df.groupby('Date_Heure_locale')[['NP', 'PA', 'MG', 'ET']].mean()
df.head()
```

```{code-cell} ipython3
# et pour être bien sûr

# maintenant value_counts() ne doit contenir que des 1
counts = df.reset_index().Date_Heure_locale.value_counts()
dups = counts[counts != 1]

if len(dups) == 0:
    print("OK !")
```

### c'est terminé

et on n'a même pas besoin d'adopter l'index puisque ça a déjà été fait par le `groupby`..

```{code-cell} ipython3
df.head(2)
```

## aperçu

notre objectif: passer le moins de temps possible pour voir une vague idée de ces données

```{code-cell} ipython3
# version simplissime: vraiment pas top

df.plot();
```

la première amélioration vient au prix d'une ligne qu'on mentionne généralement au début (autour de par exemple la ligne `import pandas as pd`)

+++

### `%matplotlib ipympl` pour des graphiques interactifs

````{admonition} limitations du format HTML statique
:class: admonition-small

il faut exécuter ceci dans Jupyter lab ou vs-code pour avoir l'interactivité  
si vous lisez cette page en HTML statique (typiquement sur `readthedocs.io`), les graphiques restent inertes, malheureusement

````

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
# sachant qu'on peut toujours choisir la taille pour une figure donnée

df.plot(figsize=(3, 3));
```

### `subplots=True`

+++

comme les échelles ne sont pas forcément les mêmes, ou pour plein d'autres raisons, on peut avoir envie de voir les données indépendamment les unes des autres

```{code-cell} ipython3
df.plot(subplots=True);
```

### `alpha=0.1`

si on insiste pour voir les 4 données dans la même vue, comme on avait fait pour commencer, il y a tellement de données en X qu'on ne voit que la dernière colonne !  
dans ces cas-là le canal alpha (la transparence) est notre meilleur allié

```{code-cell} ipython3
df.plot(alpha=0.1);
```

## les trous dans la donnée (aka nan)

à ce stade on a donc des nan - au moins dans NP, ça on en est sûr, et dans les autres colonnes peut-être aussi

```{code-cell} ipython3
# dans une colonne en particulier
df.NP.isna().sum()
```

```{code-cell} ipython3
# si on veut une information plus globale, par exemple
df.isna().sum(axis=0)
```

### comment les calculer ?

ce qu'on aimerait savoir maintenant, c'est est-ce que les 'trous' sont plutôt éparpillés ou plutôt groupés; et pour ça on va

* fabriquer une série qui contient seulement les timestamps où on a une mesure (en enlevant ceux qui correspondent à un nan, donc)
* puis on fera la **différence** avec la valeur **immédiatement voisine** (pour cela on décale les valeurs de 1 cran, et on fait la différence)

si on avait une série parfaitement pleine, on n'obtiendrait que des valeurs de "1h" dans ce résultat  
et donc en éliminant de cela les valeurs "1h", on obtient la liste des trous dans la donnée (c'est-à-dire quand y a-t-il eu un trou, et combien de temps a-t-il duré)

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

### on décale

```{code-cell} ipython3
# et du coup maintenant on peut décaler (avec shift()) les valeurs de 1 cran

NP_times_series.shift()
```

```{code-cell} ipython3
# et surtout faire la différence entre les deux, qui normalement doit donner 1h

delta = NP_times_series - NP_times_series.shift()
```

```{code-cell} ipython3
delta.head(3)
```

```{code-cell} ipython3
# il faut enlever la première ligne, évidemment
# car le shift y a mis NaT

delta = delta.iloc[1:]
```

### digression: comment fabriquer un timedelta

```{code-cell} ipython3
# c'est assez simple, on fait par exemple

pd.to_timedelta("01:00:00")
```

```{code-cell} ipython3
# ou encore, c'est assez flexible:

pd.to_timedelta(1, 'h')
```

### reprenons

nous en sommes donc au stade où on veut enlever de `delta` les valeurs correspondant à 1h

```{code-cell} ipython3
holes = delta[delta != pd.to_timedelta(1, 'h')]
```

```{code-cell} ipython3
print(f"nous avons trouvé {len(holes)} trous dans la colonne NP")
holes
```

### on les affiche

```{code-cell} ipython3
# si on veut les montrer
# c'est mieux de transformer en heures (sinon on a des nano-secondes apparemment)
# en plus comme on n'a pas une dataframe, avec le driver %matlotlib ipympl
# il faut créer une nouvelle figure

import matplotlib.pyplot as plt

plt.figure()
(holes / pd.to_timedelta(1, 'h')).plot(style=['r.']);
```

### question

utilisez le zoom pour trouver à quelle époque a eu lieu la coupure la plus longue dans l'acquisition de `NP`

```{code-cell} ipython3
# on peut le retrouver comme ceci

when = holes.idxmax()
how_long = holes.loc[when]

print(f"the longest outage was {how_long} long and occurred on {when}")
```

## un peu de lissage

on regarde cette fois la courbe 'PA'; utilisez le zoom pour regarder environ un mois

```{code-cell} ipython3
plt.figure()
PA = df.PA
PA.plot(alpha=0.4);
```

on voit que la fluctuation en tendance est obscurcie par des variations de plus haute fréquence; on va essayer de lisser ce signal pour ne conserver que la tendance de fond  

normalement si vous zoomez encore davantage, vous devriez percevoir que la haute fréquence est de l'ordre de la demie journée

+++

### rolling 

on va calculer le rolling de ce signal avec deux périodes (12h et 24h), et afficher tout cela

```{code-cell} ipython3
# rolling windowed: on essaie avec ces deux durées
# souvenez-vous que l'on a une mesure par heure

smooth24 = PA.rolling(24, center=True).mean()
smooth12 = PA.rolling(12, center=True).mean()

plt.figure()
PA.plot(alpha=0.2)

smooth12.plot(style=['g'], alpha=0.5);
smooth24.plot(style=['r'], alpha=0.5);
```

à nouveau, je vous invite à zoomer dans le graphique pour juger de la pertinence de chacune de ces deux approximations

laquelle garderiez-vous ?

+++

***
