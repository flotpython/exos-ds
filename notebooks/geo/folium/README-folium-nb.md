---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
  notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version, -jupytext.text_representation.format_version,
    -jupytext.custom_cell_magics, -language_info.version, -language_info.codemirror_mode.version,
    -language_info.codemirror_mode, -language_info.file_extension, -language_info.mimetype,
    -toc, -vscode
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

# un mot sur folium

la bibliothèque `folium` (<hhttps://python-visualization.github.io/folium/latest/>) est un utilitaire qui permet de dessiner des cartes géographiques

elle est donc souvent utilisée en conjonction avec `geopandas`

+++

## les bases

nous allons voir un exemple simplissime qui consiste à afficher des points sur une carte

+++

### une carte

et pour commencer on doit créer un objet carte

```{code-cell} ipython3
:scrolled: true

import folium

# si on veut on peut ne rien préciser du tout
# mais nous on va se centrer sur Paris

PARIS = 48.856542, 2.347614

map = folium.Map(
    location=PARIS,
    zoom_start=5,
    width=500,
    height=300,
)
map
```

### des zones

on peut facilement afficher des zones; par exemple affichons les arrondissements de Paris

* je cherche dans google avec les mots-clés "arrondissements de Paris shapefile"
* et je tombe ici <https://opendata.paris.fr/explore/dataset/arrondissements/export/>
* d'où je télécharge le fichier `arrondissements.zip` que je range dans le dossier `data/`

et après cela je peux faire tout simplement ceci

```{code-cell} ipython3
import geopandas as gpd

arrondissements = gpd.read_file("data/arrondissements.zip", encoding="utf-8")

# accessoirement ceci est une geo dataframe
type(arrondissements)
```

```{code-cell} ipython3
arrondissements.columns
```

```{code-cell} ipython3
arrondissements.head(2)
```

```{code-cell} ipython3
# pour afficher cela

map = folium.Map(
    location=PARIS,
    zoom_start=12,
)

folium.GeoJson(
    data=arrondissements,
).add_to(map)

map
```

naturellement on peut aussi, en compliquant un petit peu, mettre des couleurs différentes, ajouter des *tooltips*, etc..

par exemple:

```{code-cell} ipython3
# générateur de couleur

import random

def random_color():
    def randbyte():
        return f"{random.randint(0, 255):02x}"
    return f"#{randbyte()}{randbyte()}{randbyte()}"

# on associe une couleur à chaque arrondissement
arrondissements['color'] = arrondissements.geometry.map(lambda x: random_color())
```

```{code-cell} ipython3
:scrolled: true

# pour ajouter des zones

def paris_map():

    map = folium.Map(
        location=PARIS,
        zoom_start=11,
    )
    
    folium.GeoJson(
        data=arrondissements,
        style_function=lambda x: {"color": x["properties"]["color"]},
        tooltip=folium.GeoJsonTooltip(
            fields=["l_ar", "l_aroff"],
            aliases=["nom", "label"],
        )
    ).add_to(map)
    
    return map

paris_map()
```

### des marqueurs

pour trouver des données à afficher je retoourne ici <opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/export>

et cette fois je *download* au format GeoJson; les données sont mises à jour en temps réel, mais ce n'est pas important

```{code-cell} ipython3
velibs = gpd.read_file("data/velib-disponibilite-en-temps-reel.geojson")
velibs.head()
```

pour ajouter tous ces points, la démarche est à peu près la même que pour les arrondissements; sauf que si on le fait naïvement on tombe sur une erreur - apparemment folium n'aime pas les colonnes de type datetime64, on va l'enlever

```{code-cell} ipython3
# pour contourner une erreur signalée par folium avec les timestamps
# go figure...

if 'duedate' in velibs.columns:
    velibs = velibs.drop(columns=['duedate'])
```

```{code-cell} ipython3
# on ne voit pas grand-chose avec le look par défaut
# trops de points, les marques sont trop grosses

map = paris_map()

folium.GeoJson(
    data=velibs,
).add_to(map)

map
```

et ici aussi on peut affiner un peu et customiser le look de chaque point; on choisit de mettre un point avec une taille qui dépend du nombre de vélos disponibles

```{code-cell} ipython3
# pour ajouter des marques

map = paris_map()

folium.GeoJson(
    data=velibs,
    # on choisit le type de marker
    marker=folium.CircleMarker(),
    # et les attributs sont calculés ici
    style_function=lambda x: dict(
        color="black",
        radius=1 if not x["properties"]["capacity"]
               else 2 + 4 * (x["properties"]["numbikesavailable"]
                       /x["properties"]["capacity"])
    ),
    # on peut aussi mettre des tooltips...
    tooltip=folium.GeoJsonTooltip(
        fields=['name', 'numbikesavailable', 'capacity'],
        aliases=['nom', 'vélos dispos', 'total'],
    ),
).add_to(map)

map
```

## on peut sauver la carte !

une dernière feature très pratique, c'est qu'une fois la carte créée, on peut la sauver au format html *standalone* (plus besoin de python ni de jupyter pour l'utiliser, le fichier se charge dans un browser web)

```{code-cell} ipython3
# après l'avoir créé, ouvrez le fichier dans le browser

map.save("my-map.html")
```
