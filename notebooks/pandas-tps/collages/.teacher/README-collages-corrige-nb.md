---
jupytext:
  encoding: '# -*- coding: utf-8 -*-'
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
  title: exo collages
---

# collages

```{admonition} à télécharger
:class: warning

pour réaliser ce TP localement sur votre ordi, {download}`commencez par télécharger le zip<./ARTEFACTS-collages.zip>`
```

```{code-cell} ipython3
import pandas as pd
```

## simple critère

+++

on a trois fichiers à recoller

```{code-cell} ipython3
:cell_style: split

df1 = pd.read_csv('data/collages1.csv')
df1
```

```{code-cell} ipython3
:cell_style: split

df2 = pd.read_csv('data/collages2.csv')
df2
```

```{code-cell} ipython3
df3 = pd.read_csv('data/collages3.csv')
df3
```

comment vous feriez pour recoller les morceaux ? il s'agit d'obtenir une dataframe de 5 élèves et 4 caractéristiques

+++

on peut envisager deux versions de l'exercice, selon qu'on choisit ou non d'indexer selon le prénom

+++

### sans index

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
# prune-cell
df12 = df1.merge(df2)
df12
```

```{code-cell} ipython3
# prune-cell
df123 = pd.concat([df12, df3])
df123
```

```{code-cell} ipython3
# prune-cell

df123.to_csv("data/collages-all.csv")
```

### avec index

+++

dans un premier temps, pour chacune des trois tables, adoptez la colonne `name` comme index;

puis recollez les morceaux comme dans le premier exercice

```{code-cell} ipython3
# à vous
```

```{code-cell} ipython3
# prune-cell
df1i, df2i, df3i = df1.set_index('name'), df2.set_index('name'), df3.set_index('name')
df1i, df2i, df3i
```

```{code-cell} ipython3
# prune-cell
df12i = df1i.merge(df2i, left_index=True, right_index=True)
df123i = pd.concat([df12i, df3i])
df123i
```

## multiples critères

même idée, mais on n'a plus unicité des prénoms

```{code-cell} ipython3
m1 = pd.read_csv("data/multi1.csv")
m1
```

```{code-cell} ipython3
m2 = pd.read_csv("data/multi2.csv")
m2
```

```{code-cell} ipython3
m3 = pd.read_csv("data/multi3.csv")
m3
```

```{code-cell} ipython3
# à vous - c'est vous qui décidez comment gérer les index
# juste, à la fin on voudrait un index "raisonnable"
```

```{code-cell} ipython3
# prune-begin
```

```{code-cell} ipython3
# option 1
# sur les colonnes

m12 = pd.merge(
    m1, m2, 
    left_on=("prenom", "nom"),
    right_on=("first_name", "last_name"),
).drop(columns=["first_name", "last_name"])

m12
```

```{code-cell} ipython3
all = (
    pd.concat([
    m12, 
    m3.rename(columns={"first": "prenom", "last": "nom"})
])
    .set_index(["prenom", "nom"])
)

all
```

```{code-cell} ipython3
# option 2

# sur les index, c'est plutôt plus simple

m1i = m1.set_index(["prenom", "nom"])
m2i = (m2
    .rename(columns={"first_name": "prenom", "last_name": "nom"})
    .set_index(["prenom", "nom"])
)
m3i = (m3
    .rename(columns={"first": "prenom", "last": "nom"})
    .set_index(["prenom", "nom"])
)

all = pd.concat([pd.merge(m1i, m2i, left_index=True, right_index=True), m3i])
all
```

```{code-cell} ipython3
all.to_csv("data/multi-all.csv")
```

```{code-cell} ipython3
# prune-end
```
