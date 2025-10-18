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
---

# TP géoloc addresses

````{admonition} à télécharger
:class: warning

pour faire cette activité sur votre ordi, {download}`commencez par télécharger le zip<./ARTEFACTS-addresses.zip>`
````

ce TP vise à vous faire découvrir quelques possibilités de manipulation et d'affichage de données géographiques

+++

````{admonition} **survol**

voici les différentes étapes du TP en résumé

1. on part d'un gros paquet d'adresses parisiennes
2. on va commencer par les géolocaliser: trouver leurs latitude/longitude
3. on va ensuite les afficher sur une carte
4. puis on va ajouter dans le mélange [les 80 quartiers parisiens](https://fr.wikipedia.org/wiki/Liste_des_quartiers_administratifs_de_Paris); d'abord en les affichant simplement sur la carte
5. puis on va voir comment on ferait pour associer chaque adresse dans un quartier
6. et pour vérifier qu'on ne s'est pas trompé, on affichera les quartiers et les adresses avec des couleurs
7. enfin on verra comment passer à l'échelle pour visualiser plusieurs dizaines de milliers de points
````

+++

le résultat final sera de produire une carte interactive; [pour des raisons
techniques](https://github.com/jupyter-book/mystmd/issues/1921) on ne peut pas
l'afficher directement ici, mais pour avoir un aperçu, cherchez dans le zip
téléchargé le fichier `media/addresses-final.html` et ouvrez-le dans un
navigateur web

+++

````{admonition} librairies utilisées
on va utiliser principalement

* `geopandas`: comme son nom l'indique, `geopandas` <https://geopandas.org/en/stable/> est une librairie pour faire .. un peu de géo

  pour faire court, elle permet de manipuler un dataframe avec des coordonnées géographiques

* `folium` pour l'affichage de cartes

* et aussi au début un peu de `requests` pour envoyer des requêtes à l'API de géolocalisation
````

+++

## l'API de géolocalisation

pour obtenir des coordonnées latitude/longitude à partir d'une adresse, en France on peut utiliser un service public et gratuit:
- la documentation *swagger* est ici **<https://data.geopf.fr/geocodage/openapi>**

```{admonition} anciennes URLs
:class: dropdown
dans une version antérieure, c'était cette URL <https://adresse.data.gouv.fr/api-doc/adresse>
qui donnait le mode d'emploi de l'API de géolocalisation  
mais ! en Octobre 2025, la documentation semble en pleine refonte,  
et si l'URL existe toujours, **elle ne contient plus cette information**...
```

```{code-cell} ipython3
# for starters, for now we only need regular pandas
# we'll go to geopandas a bit later

import pandas as pd
```

vous pouvez charger le fichier `data/addresses.csv`; toutes ces adresses sont situées à PARIS

```{code-cell} ipython3
# load the data in data/addresses.csv
# and display a few first lines

addresses = pd.read_csv('data/addresses.csv')
addresses.head(4)
```

et la première chose qu'on va faire, c'est naturellement d'utiliser cette API pour géolocaliser ces adresses

+++

### un petit extrait

mais avant cela, je vous recommande de produire un fichier `addresses-small.csv` qui contient un petit extrait, disons les 10 ou 20 premières lignes; ce sera très utile pour débugger

```{code-cell} ipython3
:tags: [level_basic]

# produce a small extract into data/addresses-small.csv

# your code here
```

### une par une

+++

c'est très pratique de pouvoir faire une recherche des adresses 'une par une'; voici comment ça on s'y prendrait:

- après avoir bien lu la doc de l'API, commencez par taper dans un navigateur  
  `https://data.geopf.fr/geocodage/search/?q=3+rue+tourelles,Paris`
- observez le format de ce que vous recevez, qu'est-ce que ça peut être ?
- ajoutez `&limit=1` à l'url pour que cela donne  
  `https://data.geopf.fr/geocodage/search/?q=3+rue+tourelles,Paris&limit=1`  
  quelle différence observez-vous dans le résultat ?

+++

````{admonition} ? et & dans l'URL
:class: note dropdown

ici lorsqu'on envoie donc une requête vers l'URL  
`https://data.geopf.fr/geocodage/search/?q=18+rue+BERNARDINS,Paris&limit=1`  
les caractères `?` et `&` **jouent un rôle particulier**

pour information, la syntaxe générale c'est
```
http://le.host.name/le/path?param1=truc&param2=bidule&param3=machinechose
```

et donc de cette façon, c'est un peu comme si on appelait une fonction à distance, en lui passant
- `q=18+rue+BERNARDINS,Paris` (`q` pour *query*)
- et `limit=1` (pour avoir seulement la première réponse)

```{admonition} pour vous faire réfléchir
:class: dropdown quiz
il se passerait quoi si par exemple dans la colonne `name` il y avait un caractère `&` (imaginez la rue *Bouvart & Ratinet*)
```
````

+++

fort de toutes ces observations, allez chercher sur Internet la doc d'une librairie Python qui s'appelle `requests`  
et notamment vous devriez tomber sur une page qui commence avec cet exemple
```
>>> r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"type":"User"...'
>>> r.json()
{'private_gists': 419, 'total_private_repos': 77, ...}
```

qui devrait vous éclairer sur l'usage de base de la librairie  
(sachant que dans notre cas c'est encore plus simple puisque nous n'avons pas besoin de nous authentifier)

```{code-cell} ipython3
# requests is the swiss knife for doing http

import requests
```

```{code-cell} ipython3
# to localize ONE address
# we just need to forge the right URL

def localize_one(num, typ, nom):

    # we build the URL which directly contains the address pieces
    url = f"https://data.geopf.fr/geocodage/search/?q={num}+{typ}+{nom},Paris&limit=1"
    
    # print(f"localize_one is fetching page\n{url}")

    # sending request to the web server
    response = requests.get(url)

    # if all is OK, http returns a code in the [200 .. 300[ range
    if not (200 <= response.status_code < 300):
        print(f"WHOOPS.... {response.status_code=}")
        return

    # we can then read the answer 
    # remember it's a JSON string
    # so we can decode it on the fly
    return response.json()
```

```{code-cell} ipython3
# and here is how we could use it

localize_one(18, 'rue', 'BERNARDINS')
```

````{danger}
***MAIS*** on ne va pas faire comme ça... pourquoi d'après vous ?

```{hint}
:class: dropdown

* mesurez combien de temps ça a pris de résoudre cette adresse
    * pour cela vous pouvez utiliser la *magic* `%%timeit`
    * ou encore le module `time`, sachant que `time.time()` compte des secondes
* combien de temps il faudrait pour faire ça 30.000 fois ?
* pourquoi est-ce que c'est aussi lent de faire comme ça ?
```
````

```{code-cell} ipython3
:tags: [level_basic]

# try to estimate how long it would take 
# to resolve 20_000 addresses this way

# your code here
```

### en un seul coup

si vous avez bien lu la page qui décrit l'API, vous devez avoir remarqué qu'il y a une autre façon de lui soumettre une recherche  
c'est ce qui est indiqué ici (**cherchez `search/csv` dans la page de l'API**)
```
curl -X POST -F data=@path/to/file.csv -F columns=voie -F columns=ville https://data.geopf.fr/geocodage/search/csv/
```

+++ {"tags": ["framed_cell"]}

`````{admonition} mais comment ça se lit ce bidule ?
:class: warning dropdown
:open:

* `curl` est un programme qu'on peut utiliser directement dans le terminal pour faire des requêtes http
* dans son utilisation la plus simple, il permet par exemple d'aller chercher une page web: vous copiez l'URL depuis le navigateur, et vous la donnez à `curl`, qui peut ranger la page dans un fichier

  ```bash
  curl -o lapageweb.html http://github.com/flotpython/
  ```

* quand on utilise une API, comme on vient de le faire pour aller chercher la position de la rue des bernardins, on doit **passer des paramètres** à l'API  
et pour faire ça dans une requête http, il y a **deux mécanismes: GET et POST**


````{admonition} GET
:class: dropdown

**`GET`**: c'est le comportement par défaut de `curl`  
dans ce mode de fonctionnement les paramètres sont passés **directement dans l'URL** comme on l'a fait tout à l'heure quand on avait vu ceci
```console
localize_one is fetching page
https://data.geopf.fr/geocodage/search/?q=18+rue+BERNARDINS,Paris&limit=1
```
````

````{admonition} POST
:class: dropdown

**`POST`**: dans ce mode-là, on ne **passe plus** les paramètres dans l'URL, mais **dans les headers HTTP**  
bon je sais ça ne vous parle pas forcément, et ce n'est pas hyper important de savoir exactement ce que ça signifie, mais le point important c'est qu'**on ne va plus passer les paramètres de la même façon**
````

et donc pour revenir à notre phrase:

```
curl -X POST -F data=@path/to/file.csv -F columns=voie -F columns=ville https://data.geopf.fr/geocodage/search/csv/
```

ce qu'il se passe ici, c'est qu'on utilise `curl` pour envoyer une requête `POST` avec des paramètres `data` et `columns`  
le bon sens nous dit que

* `data` désigne un fichier csv qui contient les données à géolocaliser, une par ligne
* `columns` désigne les noms des colonnes qui contiennent (les morceaux de) l'adresse

`````

+++

#### en Python

sauf que nous, on ne veut pas utiliser `curl`, on veut faire cette requête en Python; voici comment on va s'y prendre

+++

1. en une seule requête à l'API, on va envoyer **tout le fichier** csv, en lui indiquant juste quelles sont les colonnes qui contiennent les morceaux de l'adresse
2. le résultat - toujours au format csv - pourra être également transformé en dataframe
3. qu'il ne restera plus qu'à `merge` (ou `join` si vous préférez) avec la dataframe de départ, pour ajouter les résultats de la géolocalisation dans les données de départ
   pour cette étape on peut envisager de ne garder que certaines colonnes de la géolocalisation (assez bavarde par ailleurs), je vous recommande de conserver uniquement:

   * `latitude`, `longitude` - *of course*
   * `result_city` pour pouvoir vérifier la validité des résultats - ici on devrait toujours avoir `Paris`
   * `result_type` qui devrait toujours renvoyer `housenumber`, ça permet à nouveau de vérifier qu'on a bien une adresse connue

+++

````{tip}

* pour envoyer un POST avec des paramètres, on peut faire
  ```python
  response = requests.post(url, file=some_dict, data=another_dict)
  ```

* et donc dans notre cas, puisque `data` est un paramètre de type fichier, alors que `columns` est un paramètre usuel, on fera
  ```python
  response = requests.post(url, files={'data': file_like}, data={'columns': ['col1', ...]})
  ```
  dans lequel `file_like` désigne le résultat d'un `open()` 

* enfin, `pd.read_csv` s'attend à un paramètre de type fichier, i.e. du genre de ce qu'on obtient avec `open()`  
  et du coup pour reconstruire une dataframe à partir du texte obtenu dans la requête http, on a deux choix
  1. soit on commence par sauver le texte dans un fichier temporaire (juste faire attention à choisir un nom de fichier qui n'existe pas, de préférence dans un dossier temporaire, voir le module `tempfile`)
  1. soit on triche un peu, et grâce à `io.StringIO` on peut transformer une chaine en fichier !
  
  c'est ce qu'on va faire dans notre solution, mais la première option est tout à fait raisonnable aussi
````

+++

je vous donne ma solution; si vous essayez de la chercher par vous-même,
je vous recommande d'y aller pas à pas, commencez par juste l'étape 1, puis 1 et 2, et enfin de 1 à 3  
c'est utile aussi de commencer par une toute petite dataframe pour ne pas attendre des heures pendant la mise au point...

```{code-cell} ipython3
import requests
# this one is to fake a file from a string
import io

def mass_post(filename, col_number, col_type, col_name, col_city):

    # we don't care about the index for now
    # but note that if we want to merge the result
    # with the initial data, there is a need 
    # for a unique index...

    with open(filename) as feed:
        response = requests.post(
            "https://data.geopf.fr/geocodage/search/csv/", 
            files={'data': feed},
            data={'columns': [col_number, col_type, col_name, col_city]})
    if not (200 <= response.status_code < 300):
        print(f"OOPS, got {response.status_code}")
        return None

    # this time the output is csv, not json
    # note that read_csv requires a file-like object
    # and we have a str, so io.StringIO comes to the rescue
    result = pd.read_csv(io.StringIO(response.text))

    return result


def localize_many(filename, col_number, col_type, col_name, col_city):
    df = pd.read_csv(filename)
    geoloc = mass_post(filename, col_number, col_type, col_name, col_city)
    # because we don't set an index, it is safe to merge
    geoloc = geoloc[['latitude', 'longitude', 'result_city', 'result_type']]
    return df.merge(geoloc, left_index=True, right_index=True)
```

```{code-cell} ipython3
:tags: [level_basic]

# try this code on the small sample for starters

addresses_small = localize_many("data/addresses-small.csv", "number", "type", "name", "city")
addresses_small
```

```{code-cell} ipython3
:tags: [level_basic]

# sanity check : make sure that all the entries have 
# result_city == 'Paris'
# and
# result_type == 'housenumber'

# your code
```

```{code-cell} ipython3
:tags: [level_basic]

# when you think you're ready, go full scale
# be ready to wait for at least 40-60s 

# optional: try to record the time it takes !
# tip: see for example time.time()

# addresses = localize_many("data/addresses.csv", "number", "type", "name", "city")
```

```{code-cell} ipython3
:tags: [level_basic]

# sanity check

# len(addresses)
```

```{code-cell} ipython3
:tags: [level_basic]

# at this point you should store the data
# it's just good practice, as you've done one important step of the process
# plus it takes quite some time to redo

# so: store geolocalized addresses in data/addresses-geoloc.csv

# your code
```

## afficher sur une carte

+++

à présent qu'on a une position, on va pouvoir afficher ces adresses sur une carte

et pour ça il y a plein de libs disponibles, on va choisir `folium`

si nécessaire, il faut l'installer (comment on fait déjà ?)

```{code-cell} ipython3
:tags: [level_basic]

import folium
```

pour commencer, allez chercher la documentation; le plus simple c'est de demander à google `folium python`

Question subsidiaire: comment j'ai fait d'après vous pour [embarquer cette recherche dans un lien hypertexte](https://www.google.com/search?q=folium+python) ?

et surtout (regardez les deux premiers pour l'instant):

* l'objet `Map` <https://python-visualization.github.io/folium/quickstart.html#Getting-Started>
* l'objet `Marker` <https://python-visualization.github.io/folium/quickstart.html#Markers>
* et un peu plus tard on utilisera aussi des overlays <https://python-visualization.github.io/folium/quickstart.html#GeoJSON/TopoJSON-Overlays>

```{code-cell} ipython3
# ~ chatelet

CENTER = 48.856542, 2.347614
```

### le fond de carte

```{code-cell} ipython3
:tags: [raises-exception]

# pour commencer on va recharger la dataframe précédente
import pandas as pd

addresses = pd.read_csv("data/addresses-geoloc.csv")

# et en faire un petit échantillon

addresses_small = addresses.iloc[:20]
```

```{code-cell} ipython3
:tags: [level_basic]

# créez une map centrée sur ce point et de zoom 13
# n'oubliez pas de l'afficher,
# et vérifiez que vous voyez bien Paris, 
# que vous pouvez zoomer et vous déplacer, ...

# votre code
def paris_map():
    ...

# pour l'afficher
paris_map()
```

### on ajoute les adresses

+++ {"tags": ["framed_cell"]}

pareil mais vous ajoutez les adresses qui se trouvent dans la dataframe  
éventuellement, vous pouvez comme sur l'exemple du *Getting Started* ajouter un tooltip avec l'adresse complète

```{code-cell} ipython3
:tags: [framed_cell, level_basic]

# your code here

def map_addresses(geoloc):
    """
    creates folium map centered on Paris, with the various addresses
    contained in the input dataframe shown as a marker
    """
    pass
```

```{code-cell} ipython3
# and try it out

# make sure you use A SMALL DATAFRAME because with this method
# trying to display tens of thousands addresses
# is going to be SUPER SLOOOOOW !

map_addresses(addresses_small)
```

### on sauve la carte

une fonction très sympatique de `folium`, c'est qu'on peut sauver cette carte sous la forme d'un fichier html, on dit *standalone*, c'est-à-dire autosuffisant, pas besoin de Python ni de Jupyter pour la regarder

```{code-cell} ipython3
:tags: [raises-exception]

map_small = map_addresses(addresses_small)

# je commente car à ce stade dans le notebook étudiant
# on a map_small is None et donc si on essaie de faire cela
# le notebook plante
# map_small.save("addresses-small.html")
```

et maintenant pour voir le résultat, ouvrez le fichier dans un autre tab du navigateur

+++

## les quartiers de Paris

maintenant on va ranger les adresses par quartier; pour cela nous avons dans le dossier `data/` le fichier `quartier_paris.zip` qui contiennent la définition des 80 quartiers qui recouvrent Paris intra-muros

````{admonition} source
:class: dropdown

obtenu ici <https://opendata.paris.fr/explore/dataset/quartier_paris/export/?disjunctive.c_ar>  
en choisissant le format "Shapefile"
````

ça se présente comme ceci:

```{code-cell} ipython3
# à ce stade on a besoin de geopandas
# installez-le si besoin

import geopandas as gpd
```

```{code-cell} ipython3
# ça se lit facilement
quartiers = gpd.read_file("data/quartier_paris.zip", encoding="utf8")

# et le résultat est .. une dataframe
type(quartiers)
```

```{code-cell} ipython3
# qu'on peut afficher normalement

quartiers
```

```{code-cell} ipython3
# et on peut même l'afficher sommairement avec matplotlib

# bon c'est loin d'être parfait mais ça nous suffit à ce stade
# on va voir plus loin comment incorporer ça dans la carte

quartiers.plot();
```

pour afficher cela sur la carte, il faut se livrer à une petite gymnastique

1. on construit la map comme on l'a vu jusqu'ici
3. on passe à `folium.GeoJson()` la geo-dataframe, pour créer un objet
4. qu'on ajoute dans la map

ce qui nous donne ceci:

```{code-cell} ipython3
def paris_map():
    """
    create a map of Paris with its 80 quartiers
    """
    map = folium.Map(
        location=CENTER,
        zoom_start=13,
        # width='80%',
    )

    # create a folium JSON object from the geo df
    folium.GeoJson(
        data=quartiers,
        # optionnally we could also tweak things on the way
        # try to uncomment these
        # style_function=lambda x: {"fillColor": "#45a012", "color": "#881212"}
        # the name is in the l_qu column
        # tooltip=folium.GeoJsonTooltip(fields=['l_qu'], aliases=['quartier']),
    # and add it to the map
    ).add_to(map)

    # and that's it
    return map
```

```{code-cell} ipython3
paris_map()
```

### un peu de couleurs

+++

maintenant c'est à vous: il s'agit d'améliorer cela pour ajouter des couleurs aux quartiers:

+++

1. écrivez une fonction `random_color` qui renvoie une couleur au hasard, i.e. une chaine comme `#12f285`
1. ajoutez dans la dataframe `quartiers` une colonne contenant une couleur aléatoire
1. écrivez `map_addresses_in_quartiers_2`, une variante qui affiche les quartiers avec chacun une couleur

+++

### couleurs: étape 1

```{code-cell} ipython3
# in order to display a number in hexadecimal, you can use this 

x = 10
f"{x:02x}"
```

```{code-cell} ipython3
:tags: [level_basic]

# your code here

def random_color():
    """
    returns a random color as a string like e.g. #12f285
    that is to say containing 3 bytes in hexadecimal
    """
    # of course this is not the right answer
    return "#12f285"
```

```{code-cell} ipython3
random_color(), random_color()
```

### couleurs: étape 2

```{code-cell} ipython3
:tags: [level_basic]

# add a random color column in quartiers

# your code here
```

```{code-cell} ipython3
quartiers.head(3)
```

### couleurs: étape 3

+++

````{tip}
ça m'a pris un peu de temps à trouver comment faire, voici un indice

<https://stackoverflow.com/questions/72983410/folium-geojson-how-to-apply-the-stylefunction-within-a-loop>
````

```{code-cell} ipython3
:tags: [level_basic]

# display the quartiers with their individual color

# your code

def paris_map():
    """
    create a map of Paris with its 80 quartiers
    each quartier is shown in its individual color
    """
    pass
```

```{code-cell} ipython3
# display it
paris_map()
```

## spatial join

+++

ce qu'on aimerait bien faire à présent, c'est de trouver le quartier de chaque adresse  
c'est-à-dire en pratique de rajouter dans la dataframe des adresses une ou des colonnes indiquant le quartier

et pour faire cela il existe un **outil très intéressant** dans geopandas [qui s'appelle le *spatial join* et qui est décrit ici](https://geopandas.org/en/stable/gallery/spatial_joins.html#Spatial-Joins)

en deux mots, l'idée c'est de faire comme un JOIN usuel (ou un `pd.merge()` si vous préférez)  
mais pour décider si on doit aligner deux lignes (une dans la df de gauche et l'autre dans la df de droite):
- au lieu de vérifier **l'égalité** entre deux colonnes
- on va cette fois utiliser un **prédicat** entre deux colonnes géographiques, comme par exemple ici le prédicat **`contains`**

ce qui signifie, en pratique, qu'on va faire ceci

1. transformer la dataframe d'adresses en une `GeoDataFrame` et remplacer les colonnes `latitude` et `longitude` par une colonne `position`, cette fois dans un format connu de `geopandas`
2. et ainsi on pourra appliquer un *spatial join* entre la (géo)dataframe d'adresses et la (géo)dataframe des quartiers, en choisissant ce prédicat **`contains`**
3. et du coup modifier la carte pour afficher les adresses dans la bonne couleur - celle du quartier - pour vérifier qu'on a bien fait correctement le classement en quartiers

on doit donc obtenir autant de ligne que d'adresses, mais avec une ou des colonnes en plus (couleur, nom du quartier, ...) qui caractérisent le quartier dans lequel se trouve l'adresse

+++

### spatial join: étape 1

je vous donne le code; ce qu'il faut savoir notamment c'est qu'en `geopandas` il y a la notion de 'colonne active', celle qui contient les informations géographiques; ça n'est pas forcément hyper-intuitif la première fois...

<https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_geometry.html>

```{code-cell} ipython3
def convert_lat_lon(df):
    """
    the input df is expected to have 2 columns named 'latitude' and 'longitude'

    this function will create a GeoDataFrame based on that, where 'latitude' and 'longitude'
    are replaced by a new column named 'position' 
    also this new column becomes the active geometry for future operations 
    (in our case the spatial join)
    """

    # we need a geopandas-friendly df
    geo_df = gpd.GeoDataFrame(df)

    # beware, here LONGITUDE comes first !
    geo_df['position'] = gpd.points_from_xy(df.longitude, df.latitude)

    # it would make sense to clean up
    # BUT
    # our map-production code relies on these columns, so...
    # del geo_df['latitude']
    # del geo_df['longitude']

    # declare the new column as the active one
    geo_df.set_geometry('position', inplace=True)

    # a technicality: turns out the shapefile was created
    # withthis coordinate reference system
    geo_df.set_crs(epsg=4326, inplace=True)

    return geo_df
```

```{code-cell} ipython3
:tags: [raises-exception]

# let's apply that to our small input

geoaddresses_small = convert_lat_lon(addresses_small)
```

```{code-cell} ipython3
:tags: [raises-exception]

# we will also need to set the active column in the quartiers (geo)dataframe

quartiers.set_geometry('geometry', inplace=True)
```

### spatial join: étape 2

Il ne nous reste plus qu'à faire ce fameux *spatial join*, je vous laisse trouver le code pour faire ça

```{code-cell} ipython3
:tags: [level_basic]

# spatial join allows to extend the addresses dataframe
# with quartier / arrondissement information

# your code

def add_quartiers(gdf):
    """
    given an addresses geo-dataframe, 
    (i.e. typically produced as an output of convert_lat_lon)
    this function will use spatial join with the quartiers information
    and return a copy of gdf extended with columns such as
    l_qu : name of the quartier
    c_ar : arrondissement number
    color: the (random) color of that quartier
    ...

    """
    # this is not the right answer...
    return gdf
```

```{code-cell} ipython3
:tags: [raises-exception]

# try your code

# xxx you can safely ignore this warning...
# UserWarning: CRS mismatch between the CRS of left geometries and the CRS of right geometries

geoaddresses_small_extended = add_quartiers(geoaddresses_small)
geoaddresses_small_extended.head(2)
```

```{code-cell} ipython3
:tags: [raises-exception]

# verify your code

# make sure you have the right number of lines in the result

geoaddresses_small_extended.shape
```

### spatial join: étape 3

on va donc maintenant récrire `map_addresses`; la logique reste la même mais on veut afficher chaque adresse avec une couleur qui provient de son quartier

comme vous allez le voir, l'objet `folium.Marker` ne peut pas s'afficher avec une couleur arbitraire - il semble qu'il y ait [seulement une petite liste de couleurs supportées](https://stackoverflow.com/questions/75011160/how-do-assign-color-to-folium-map-based-on-another-column-value)

pour contourner ça, utilisez à la place un objet de type `folium.CircleMarker`

```{code-cell} ipython3
:tags: [level_basic]

# rewrite map_addresses so that each address is shown 
# in the color of its quartier

def map_addresses(gdf):
    """
    (slightly) rewrite the first version of this function

    your input is now a geopandas dataframe, with the information
    about the 'quartier'

    and your job is to display all the addresses on the map, now with
    the color of the 'quartier'

    return a folium map of paris with the adresses displayed
    """
    return
```

```{code-cell} ipython3
:tags: [raises-exception]

# test the new function

map = map_addresses(geoaddresses_small_extended)

map
```

### on sauve la carte

c'est sans doute un bon moment pour sauver tout ce qu'on a fait:

- sauvez la geo-dataframe dans un fichier `addresses-small-extended.csv`
- sauvez la carte au format html (même nom sinon) pour une utilisation en *standalone* (par exemple pour la publier sur un site web indépendant des notebooks et de jupyter et tout ça)

```{code-cell} ipython3
:tags: [level_basic]

# votre code
```

## on clusterise

pour pouvoir passer à l'échelle, il est indispensable de *clusteriser*; c'est-à-dire de grouper les points en fonction du niveau de zoom; voyons ce que ça donne

ne perdez pas de temps à chercher le code vous-même, c'est un peu *hacky* comme on dit, voici comment il faut faire

```{code-cell} ipython3
from folium import plugins

def map_addresses(gdf):

    # start like before
    if 'human' not in gdf.columns:
        # create a column with a human-readable address
        gdf['human'] = gdf['number'].astype(str) + ', ' + gdf['type'] + ' ' + gdf['name']

    map = paris_map()


    # we need a JavaScript function...
    # this is required to get  good performances
    callback = """
function (row) {
  // if you need to debug it
  // console.log(row)
  let circle = L.circleMarker(
      // the position
      new L.LatLng(row[0], row[1]),
      // styling
     {color: row[3], radius: 8},
    )
  // add the tooltip
  circle.bindTooltip(row[2]).openTooltip()
  return circle
}
"""

    # compute an extract with fewer columns
    # not strictly necessary but easier to deal with column names
    extract = gdf[['latitude', 'longitude', 'human', 'color']]
    cluster = plugins.FastMarkerCluster(
        extract, callback=callback,
        # nicer behaviour
        disableClusteringAtZoom=18,
    ).add_to(map)

    return map
```

### sur l'échantillon

```{code-cell} ipython3
:tags: [raises-exception]

# let's first test it on the small extract

map_addresses(geoaddresses_small_extended)
```

### sur le dataset entier

```{code-cell} ipython3
:tags: [raises-exception]

# and if all goes well we can try and display the full monty

# first prepare the full dataset
geoaddresses = add_quartiers(convert_lat_lon(addresses))

# and create the map from that
final_map = map_addresses(geoaddresses)

# display the map
final_map
```

```{code-cell} ipython3
:tags: [raises-exception]

# makes sense to save the hard work

# geoaddresses.to_csv("addresses-final.csv")
# final_map.save("addresses-final.html")
```

## références

le jeu de données utilisé ici provient à l'origine de
<https://nakala.fr/10.34847/nkl.3038f62v#e6f991e37ab1fadb388262b57472a703ba379d48>, légèrement retravaillé pour les besoins du TP

+++

***
