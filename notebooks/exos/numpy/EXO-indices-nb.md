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
nbhosting:
  title: utiliser les indices
---

```{code-cell} ipython3
import numpy as np
```

# broadcasting / dimensions

+++

on va commencer par quelques rappels et astuces

+++

## broadcasting

+++

un trait qui sera abordé en cours, mais qu'on peut mettre en évidence facilement

```{code-cell} ipython3
# un tableau en ligne
row = np.array([0, 1000, 2000, 3000])
# un tableau en colonne
col = np.array([[0], [10], [20]])
```

```{code-cell} ipython3
row
```

```{code-cell} ipython3
col
```

eh bien ces deux tableaux, bien que n'ayant pas la même forme, peuvent s'ajouter !

```{code-cell} ipython3
row + col
```

## reshaping

+++

pour fabriquer le tableau `col` ci dessus, on aurait pu procéder de plein d'autres façons

```{code-cell} ipython3
# en partant des données 'à plat'
raw = np.array([0, 10, 20])
```

```{code-cell} ipython3
# on aurait pu produire la forme de `col` comme ceci
# dans un reshape, le -1 est calculé pour boucher le trou
col1 = raw.reshape((-1, 1))
col1
```

```{code-cell} ipython3
# avec newaxis
col2 = raw[:, np.newaxis]
col2
```

## `indices`

+++

la fonction `np.indices` est très pratique pour obtenir les rangs dans le tableau

```{code-cell} ipython3
# par exemple
I, J = np.indices((3, 4))
```

```{code-cell} ipython3
I, J
```

# exercices

+++

Voici maintenant de quoi mettre ces astuces en pratique

+++

## table de multiplication

+++

Produisez le tableau de la table de multiplication des entiers entre 1 et n

On peut le faire de au moins 3 façons (cf les 3 premières sections ci-dessus)

```{code-cell} ipython3
:tags: [level_advanced]

N = 5

# à vous
```

## échiquier

+++

### base - v1

+++

On veut écrire une fonction qui produit un échiquier

ex. avec `checkers(3, 4)`

|  |  |  |  |
|--|--|--|--|
| 0| 1| 0| 1|
| 1| 0| 1| 0|
| 0| 1| 0| 1|

```{code-cell} ipython3
:tags: [level_advanced]

# à vous

def checkers():
    """
    vous avez le droit d'écrire le docstring :)
    """
    ...
```

```{code-cell} ipython3
:tags: [raises-exception, hide-output, level_basic]

# ceci doit afficher True

np.all(checkers(3, 4) == np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1]]))
```

### v2 - pareil, mais doit retourner des booléens

```{code-cell} ipython3
:tags: [level_advanced]

# à vous

def checkers():
    ...
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# ceci doit afficher True

np.all(checkers(3, 4) == np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1]]))
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# ceci doit afficher True

checkers(3, 4).dtype == bool
```

### affichage

+++

comment feriez-vous pour afficher le tableau comme un damier ?

**[indice]** voyez `plt.imshow()`

```{code-cell} ipython3
:tags: [level_advanced]

# à vous
...
```

### paramètrer le coin

+++

Pour corser un peu, on ajoute un paramètre optionnel qui indique, lorsqu'il est True, qu'on veut que l'échiquer est inversé

ex. avec `checkers(3, 4, True)`

|  |  |  |  |
|--|--|--|--|
| 1| 0| 1| 0|
| 0| 1| 0| 1|
| 1| 0| 1| 0|

mais les appels avec seulement deux paramètres continuent à fonctionner comme avant

```{code-cell} ipython3
:tags: [level_advanced]

# à vous
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# ceci doit afficher True

np.all(checkers(3, 4) == np.array([[0,1,0,1],[1,0,1,0],[0,1,0,1]]))
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# ceci doit afficher True

np.all(checkers(3, 4, True) == ~(checkers(3, 4)))
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# pour débugger
checkers(3, 4)
```

```{code-cell} ipython3
:tags: [raises-exception, level_basic, hide-output]

# pour débugger
checkers(3, 4, True)
```

### tester

+++

On veut maintenant tester que si on ajoute ces deux formes on n'obtient que des 1

```{code-cell} ipython3
:tags: [level_advanced]

# à vous d'écrire le code qui vous permettra de vous en assurer
```

## escaliers

+++

écrivez une fonction qui retourne une espèce de pyramide escalier comme ceci

si le paramètre est 2, on retourne un tableau de taille $2*n+1$

`stairs(2)`

| | | | | |
|-|-|-|-|-|
|0|1|2|1|0|
|1|2|3|2|1|
|2|3|4|3|2|
|1|2|3|2|1|
|0|1|2|1|0|

+++

### quelques indices

+++

toujours pour le cas où n=2, voici quelques phrases que je vous laisse lire

```{code-cell} ipython3
I, J = np.indices((5, 5))
```

```{code-cell} ipython3
# si on décale, retourne, et applique abs()
abs(2-I), abs(2-J)
```

```{code-cell} ipython3
# si on les ajoute
abs(2-I) + abs(2-J)
```

```{code-cell} ipython3
# on y est presque
4-(abs(2-I) + abs(2-J))
```

```{code-cell} ipython3
:tags: [level_advanced]

# à vous de mettre tout cela ensemble

def stairs(n):
    ...
```

```{code-cell} ipython3
:tags: [level_advanced]

# comment feriez-vous pour afficher le résultat visuellement ?

# à vous
```

***
