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
  title: "donn\xE9es coronavirus"
---

# les données coronavirus

+++

## Le dashboard de Johns Hopkins

+++

Le département *Center for Systems Science and Engineering* (CSSE), de l'Université Johns Hopkins, publie dans un dépôt github <https://github.com/CSSEGISandData/COVID-19> les données dans un format assez brut. C'est très détaillé et touffu :

```{code-cell} ipython3
# le repo github
official_url = "https://github.com/CSSEGISandData/COVID-19"
```

Le README mentionne aussi un *dashboard*, qui permet de visualiser les données en question. Il me semble que l'URL change tous les jours au fur et à mesure des updates, donc le mieux c'est d'aller visiter cette page directement.

+++

## un jeu de données intéressant

+++

Pour ma part j'ai préféré utiliser un dépôt de seconde main, qui consolide en fait les données du CS
SE, pour les exposer dans un seul fichier au jormat JSON. Cela est disponible dans ce second dépôt github <https://github.com/pomber/covid19>; la donnée est mise à jour quotidiennement
 et est disponible - en Avril 2021 - (voir le README) à cette URL:

```{code-cell} ipython3
json_url = "https://pomber.github.io/covid19/timeseries.json"
```

Pour aller chercher cette donnée on utilise le module `requests`, qui n'est pas dans la librairie standard, donc si nécessaire on l'installe avec cette commande

+++

## les dépendances

```{code-cell} ipython3
!pip install requests
```

## les données brutes

+++

Comme c'est du JSON, on peut charger ces données en mémoire comme ceci

```{code-cell} ipython3
# pour aller chercher l'URL
import requests

# allons-y
req = requests.get(json_url)
```

```{code-cell} ipython3
# pour vérifier que la connexion s'est bien passé
req.ok
```

```{code-cell} ipython3
# en utilisant la property `text` on décode en Unicode
decoded = req.json()
```

## à quoi ça ressemble

```{code-cell} ipython3
import pandas as pd
```

```{code-cell} ipython3
type(decoded)
```

```{code-cell} ipython3
import itertools
list(itertools.islice(decoded.keys(), 2))
```

## d'un seul coup ?

```{code-cell} ipython3
# pd.DataFrame(decoded)
```

## une dataframe par pays

```{code-cell} ipython3
france_records = decoded['France']
```

```{code-cell} ipython3
df_france = pd.DataFrame(france_records)
```

```{code-cell} ipython3
df_france
```

## on consolide

```{code-cell} ipython3
# on va faire comme ça avec tous les pays
# mais attention if faut ajouter une colonne 'country' 
# sinon l'info est perdue

def country_df(country, country_records):
    country_df = pd.DataFrame(country_records)
    country_df['country'] = country
    return country_df


df = pd.concat([
    country_df(country, country_records)
    for country, country_records in decoded.items()
])
```

```{code-cell} ipython3
df
```

## les dates

```{code-cell} ipython3
# le type du champ date n'est pas le bon, bien sûr

df.date.dtype
```

```{code-cell} ipython3
# du coup on a le réflexe de convertir

df.date = pd.to_datetime(df.date)
```

```{code-cell} ipython3
df.date.dtype
```

## l'index

+++

il y a plein de façons d'indexer bien sûr, mais il me semble que la plus naturelle ce serait ceci

```{code-cell} ipython3
# un cas typique où le MultiIndex s'impose...
df = df.set_index(['country', 'date'])
```

```{code-cell} ipython3
df
```

```{code-cell} ipython3
# on met de coté les 3 colonnes
columns = df.columns
```

## retrouver un pays

+++

du coup maintenant si on voulait retrouver les données d'un pays on ferait juste

```{code-cell} ipython3
:hide_input: false

df_france = df.loc['France']; df_france
```

## cumulatif vs instantané

```{code-cell} ipython3
df.columns, df.index.levels[0]
```

```{code-cell} ipython3
df
```

on ne peut pas calculer la version instantanée en faisant simplement un décalage sur les colonnes
car dans ce cas les pays vont se polluer les uns les autres...

```{code-cell} ipython3
# ceci fonctionne mal aux extrémités des pays
"""
df_diff = df.copy()

for column in columns:
    df_diff[column] = (df_diff[column] - df_diff[column].shift()).rolling(7).mean()
""";
```

```{code-cell} ipython3
# il faut d'abord un-stacker pour avoir une colonne par type x pays
df_diff = df.copy()
df_diff = df_diff.unstack(level=0)
```

```{code-cell} ipython3
# maintenant on peut faire glisser et calculer la variation
# et tant qu'on y est on lisse tout cela sur une semaine
df_diff = (df_diff - df_diff.shift()).rolling(7).mean()
```

```{code-cell} ipython3
# il se passe un truc bizarre avec les 'new cases' en France 
# vers le 20 Mai 2021 - probablement une nouvelle façon de compter
# en tous cas une chute spectaculaire sur une seule journée
# et du coup la dérivée donne un chiffre fortement négatif
df_diff[df_diff <= 0] = 0
```

```{code-cell} ipython3
# df_diff
```

```{code-cell} ipython3
# on enlève la première semaine du coup car après lissage elle vaut nan
# xxx utiliser dropna plutôt ce serait moins fragile
df_diff = df_diff.iloc[7:]
```

```{code-cell} ipython3
# maintenant on peut remettre dans le même format que notre df de départ
# mais un simple stack() ne suffit pas
# il faut aussi remettre (les niveaux de) l'index dans le bon ordre
df_diff = df_diff.stack(level=1).reorder_levels([1, 0])
```

```{code-cell} ipython3
# pour vérifier qu'on a bien la même structure que df
df_diff.columns, df_diff.index.levels[0]
```

```{code-cell} ipython3
df_diff.loc['France'].plot();
```

## quelques dessins

```{code-cell} ipython3
import matplotlib.pyplot as plt
```

en version super paresseuse, on peut afficher un pays comme ceci

```{code-cell} ipython3
:cell_style: split

df.loc['France'].plot();
```

```{code-cell} ipython3
:cell_style: split

df_diff.loc['France'].plot();
```

## un peu d'interaction - un pays

+++

on a vu plus haut qu'on pouvait afficher un pays juste en extrayant `df.loc[country]`, sur laquelle on fait juste `plot()`

du coup on peut faire un premier dashboard très simple comme ceci

```{code-cell} ipython3
# la fonction qui affiche un pays, en choisissant la ou les catégories
def display_corona1(df, 
                    country:str, 
                    confirmed:bool, deaths:bool, recovered:bool):
    focus = df.loc[country]
    for column in ('confirmed', 'deaths', 'recovered'):
        # eval('confirmed') retourne la valeur de confirmed
        if not eval(column):
            del focus[column]
    focus.plot()
```

```{code-cell} ipython3
# pour vérifier que ça marche avec un pays
# display_corona1(df, 'France', False, True, False)
```

```{code-cell} ipython3
from ipywidgets import interact, fixed, Checkbox, Dropdown, fixed

def one_country(df):
    interact(display_corona1, 
         df=fixed(df),
         country=Dropdown(value='France', options=list(decoded.keys()), description='Country'),
         confirmed=Checkbox(value=True, description='Confirmed cases'),
         deaths=Checkbox(value=False, description='Deaths'),
         recovered=Checkbox(value=False, description='Recovered'),
        );
```

```{code-cell} ipython3
one_country(df)
```

```{code-cell} ipython3
one_country(df_diff)
```

## un peu d'interaction - plusieurs pays

+++

pareil mais on peut choisir plusieurs pays

+++

### une première idée - qui ne marche pas

+++

alors c'est vrai qu'**on peut passer une liste** à `.loc[]`

```{code-cell} ipython3
df.loc[['France', 'Germany']]
```

mais malheureusement si on essaye d'utiliser `display_corona1` telle quelle en lui passant une liste de pays, ça donne ceci, **ça n'est pas ce qu'on veut**:

```{code-cell} ipython3
# si on la lance avec deux pays, la sélection fonctionne
# mais les deux pays sont présentés .. l'un après l'autre !

display_corona1(df_diff, ['France', 'United Kingdom'], False, True, False)
```

### mise en forme

+++

Une façon de faire, c'est de retrier/réindexer pour avoir un multi-index sur les colonnes 

|       | confirmed |         |  deaths |         | 
|-------|-----------|---------|---------|---------|
|       | France    | Germany |  France | Germany | 
| date1 |  3        |  2      |   1     |  0      |
| date2 |  4        |  3      |   2     |  1      |

```{code-cell} ipython3
# et pour ça, unstack() c'est magique:
df.loc[['France', 'Germany']].unstack(0)
```

### du coup ça donne ceci

```{code-cell} ipython3
# with 3.9 one can write 
# def foo(countries: list[str]):
# but on cacalc this is not yet supported
from typing import List

def display_corona(df,
                   countries: List[str],
                   confirmed: bool, deaths, recovered):
    # beware that SelectMultiple is going to pass us tuples
    countries = list(countries)
    focus = (df.loc[countries]
             .unstack(0))
    colnames =     ('confirmed', 'deaths', 'recovered')
    colselecteds = (confirmed, deaths, recovered)
    selected = [colname 
                for colname, colselected in zip(colnames, colselecteds)
                if colselected]
    focus = focus.loc[:, selected]
    focus.plot()
```

```{code-cell} ipython3
# display_corona(['Germany', 'Belgium'], False, True, False)
```

```{code-cell} ipython3
from ipywidgets import interact, fixed, Checkbox, Dropdown, SelectMultiple

countries_chooser = SelectMultiple(
    value=['France', 'Germany', 'United Kingdom'],
    options=list(decoded.keys()),
    description='Countries',
    rows=10)

def multi_countries(df):
    interact(display_corona, 
         df=fixed(df),
         countries=countries_chooser,
         confirmed=Checkbox(value=False, description='Cases'),
         deaths=Checkbox(value=True, description='Deaths'),
         recovered=Checkbox(value=False, description='Recovered'),
        );
```

```{code-cell} ipython3
multi_countries(df)
```

```{code-cell} ipython3
multi_countries(df_diff)
```

## choisir les dates

+++

en tirant profit (du widget `DatePicker`)[https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#Date-picker]

on ajoute des boutons pour pouvoir choisir la date de début et la date de fin

+++

### les types impliqués

```{code-cell} ipython3
from ipywidgets import interact, fixed, Checkbox, Dropdown, SelectMultiple, DatePicker
```

juste pour voir le type retourné par DatePicker

```{code-cell} ipython3
def display_date(chosen_date):
    print(f"{type(chosen_date)=}")
    print(f"{chosen_date=}")

# select a date to see the returned type
# which is datetime.datetime
interact(display_date, 
         chosen_date=DatePicker(description='pick a date'));
```

et dans la dateframe on a des `pd.Timestamp`

+++

### ce qui donne

```{code-cell} ipython3
def display_corona_dates(
        df, countries: List[str],
        confirmed: bool, deaths, recovered,
        date_from=None, date_to=None,
        figsize=None):
    if not (confirmed or deaths or recovered):
        print("need to select at least one category")
        return
    countries = list(countries)
    focus = df.loc[countries].unstack(0)
    # so as we just saw, date_from as passed by DatePicker is a datetime.datetime
    # and we need to convert that into a pd.Timestamp when needed
    date_from = None if not date_from else pd.Timestamp(date_from)
    date_to = None if not date_to else pd.Timestamp(date_to)
    # selecting on the dates can be done through a simple slice in .loc[]
    focus = focus.loc[date_from:date_to]
    # selecting on the columns with another .loc[]
    colnames =     ('confirmed', 'deaths', 'recovered')
    colselecteds = (confirmed, deaths, recovered)
    selected = [colname 
                for colname, colselected in zip(colnames, colselecteds)
                if colselected]
    focus = focus.loc[:, selected]
    figsize = (12, 5) if figsize is None else figsize
    focus.plot(figsize=figsize)
```

```{code-cell} ipython3
# display_corona_date(['Germany', 'Belgium'], False, True, False)
```

```{code-cell} ipython3
from ipywidgets import interact, fixed, Checkbox, Dropdown, SelectMultiple

def multi_countries_dates(df):
    interact(display_corona_dates, 
             df=fixed(df),
             countries=countries_chooser,
             confirmed=Checkbox(value=False, description='Cases'),
             deaths=Checkbox(value=True, description='Deaths'),
             recovered=Checkbox(value=False, description='Recovered'),
             date_from = DatePicker(description='from'),
             date_to   = DatePicker(description='to'),
             figsize=fixed(None),
        );
```

```{code-cell} ipython3
multi_countries_dates(df)
```

```{code-cell} ipython3
multi_countries_dates(df_diff)
```

## les widgets un peu arrangés

+++

mais c'est pas très beau...

```{code-cell} ipython3
from ipywidgets import HBox, VBox, interactive_output
from IPython.display import display

def dashboard_and_bindings():
    countries_chooser = SelectMultiple(
        value=['France', 'United Kingdom', 'Germany'],
        options=list(decoded.keys()),
        description='Countries',
        rows=10)
    diff      = Checkbox(value=True, description="instantané (pas cumulé)")
    confirmed = Checkbox(value=False, description='Cases')
    deaths    = Checkbox(value=True, description='Deaths')
    recovered = Checkbox(value=False, description='Recovered')
    date_from = DatePicker(description='from')
    date_to   = DatePicker(description='to')

    dashboard = HBox([countries_chooser,
                     VBox([diff, confirmed, deaths, recovered, date_from, date_to])
    ])
    bindings = dict(countries=countries_chooser, diff=diff, confirmed=confirmed, deaths=deaths,
                        recovered=recovered, date_from=date_from, date_to=date_to)
    return dashboard, bindings
```

```{code-cell} ipython3
# malheureusement on ne peut pas utliser un simple wrapper
#def display_corona_dates_diff(diff, *args):
#    df = df if not diff else df_diff
#    display_corona_dates(*args)
    
def display_corona_dates_diff(
        countries: List[str],
        diff: bool,
        confirmed: bool, deaths, recovered,
        date_from=None, date_to=None):
    local_df = df if not diff else df_diff
    display_corona_dates(local_df, countries,
                         confirmed, deaths, recovered,
                         date_from, date_to,
                         figsize=(12, 6))
```

```{code-cell} ipython3
dashboard, bindings = dashboard_and_bindings()

display(dashboard)
interactive_output(display_corona_dates_diff, bindings)
```

***
