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
  show_up_down_buttons: true
  title: exo bornes
---

# `stack()` pour énumérer une liste

```{code-cell} ipython3
import pandas as pd
from head import head
```

```{code-cell} ipython3
# pour information seulement (on a des .csv maintenant)
# pour lire les excel au format .xlsx il faut importer ceci

# !pip install openpyxl
```

on a trois tables comme ceci

```{code-cell} ipython3
df1 = pd.read_csv('data/bornes.csv', sep=';')
df2 = pd.read_csv('data/bornes2.csv', sep=';')
df3 = pd.read_csv('data/bornes3.csv', sep=';')
```

```{code-cell} ipython3
:cell_style: split

df1
```

```{code-cell} ipython3
:cell_style: split

df2
```

```{code-cell} ipython3
df3
```

on veut transformer cela pour aboutir à ceci; une ligne par borne

| ville | borne | op_name |
|-|-|-|
| Paris | 201 | Tesla |
| Paris | 202 | City EV| 
|...| ...| ...|

+++

il s'agit donc de démêler l'écheveau pour fabriquer une table qui a 6 lignes, et pour chaque ligne l'opérateur de la borne

+++

## indices

* on a vu dans le cours que sur un objet Series on pouvait avoir besoin
  occasionnellement d'utiliser l'attribut `str`
* ici on a envie de passer par un objet liste; notamment je vous rappelle
  * la méthode `replace()` sur les chaines de caractères
  * la méthode `split()` sur les chaines de caractères
* une fois que vous êtes arrivés à mettre une liste dans une cellule d'une Series, 
  il peut être intéressant de remplacer ce contenu par .. un objet Series
* vous pourrez ensuite invoquer la méthode `.stack()` sur la Series englobante

+++

----

```{code-cell} ipython3
# à vous de jouer
```
