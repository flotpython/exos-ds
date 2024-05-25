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

# un mot sur streamlit

la bibliothèque `streamlit` (<https://streamlit.io/>) est un utilitaire qui permet de réaliser rapidement des applis de type *dashboard* - c'est-à-dire par exemple une visualisation interactive où on peut faire varier différents paramètres d'entrée, pour explorer interactivement des données

+++

## pour quoi faire ?

pour vous rendre compte rapidement de ce qu'on peut en faire, je vous recommande ceci

```bash
pip install streamlit
streamlit hello
```

mais voyons un peu comment ça marche...

+++

## c'est du Python, mais ..

le code est du Python, avec toutefois une particularité car il ne se lance pas, 
comme on en a l'habitude, avec `python monscript.py`, mais avec 

```bash
streamlit run monscript.py
```

qui va ouvrir une fenêtre dans le navigateur web - un peu comme `jupyter lab` finalement

bien sûr, il faut d'abord avoir installé avec `pip install streamlit`

+++

## les variables peuvent être interactives

imaginons que vous voulez pouvoir modifier interactivemement une variable de votre code

si votre programme en pur Python est

```python
# the temperature
T = 10

# ... on fait des trucs où T intervient
```

vous remplacez ça en streamlit par

```python
import streamlit as st

# the temperature
T = st.slider("temperature", value=1, min_value=1, max_value=10, step=1)

# ... ici T vaut ce que vous avez réglé avec le curseur
```

qui va créer un curseur graphique pour pouvoir régler T entre 1 et 10 (en commençant à 1)

+++

## la logique globale, et le cache

streamlit va tout simplement réexécuter l'intégralité du script à chaque fois qu'on change un des réglages; c'est cela qui rend l'application interactive

à cause de cette particularité, on a parfois besoin de "cacher" certaines opérations, pour ne pas les refaire à chaque fois;  
pensez par exemple au chargement d'une grosse table de données, on ne veut pas attendre 10s à chaque fois...  
pour ce genre d'usages il y a un utilitaire qui se présente comme ceci

```python
do this only once, not at each re-run

@st.cache_data
def load_url(url):
    return gpd.read_file(url)

earthquakes = load_url("data/significant-earthquake-database.geojson")
```

+++

## fonctions spécialisées

ainsi on utilise systématiquement les fonctions d'affichage de `streamlit` pour les affichages;  
c'est-à-dire qu'on n'utilise jamais `print()` mais des fonctions telles que 

* `st.text()` pour afficher un message  et plein d'autres variantes (`title`, `markdown`, ...)
* `st.dataframe()` pour afficher une dataframe
* `st.pyplot()` pour afficher une figure construite avec matplotlib
  * mais voyez aussi des outils natifs streamlit comme `st.line_chart` et similaires
* de quoi créer des widgets usuels (slider comme ci-dessus, dropdown, etc etc)
* de quoi les assembler en colonnes ou lignes pour le layout
* etc etc.. c'est très complet
* et en plus on trouve des plugins, comme par exemple pour la librairie `folium`
  qui fait de l'affichage géographique - voir <https://folium.streamlit.app/>

+++

### cheatsheet
pour une liste plus complète, une cheatsheet - écrite, comme il se doit, en streamlit - est dispo ici:

<https://cheat-sheet.streamlit.app/>

+++

### la doc complète

si vous n'avez pas trouvé dans la cheatsheet, vous avez toujours bien sûr la version complète de la doc ici:

<https://docs.streamlit.io/library/api-reference>

+++

## deux exemples

vous trouverez enfin dans ce même dossier deux exemples (si nécessaire: {download}`télécharger le zip<./ARTEFACTS-streamlit.zip>`)

* [la fonction sinus](./streamlit-sinux.py)
  hyper basique: on peut régler la fréquence et l'amplitude
* [approximation de taylor](./streamlit-taylor.py)  
  un peu plus évolué, on affiche l'approximation de `sin(x)` par une série de Taylor, et on choisit le degré
