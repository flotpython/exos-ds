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
  title: Taylor et autograd
---

# Taylor (1/3): intro à autograd

+++

le package est ici

* sources https://github.com/HIPS/autograd

+++

## installation

+++

donc comme toujours on l'installe avec `pip`

```{code-cell} ipython3
# si nécessaire
# %pip install autograd
```

## comment s'en servir

```{code-cell} ipython3
import autograd.numpy as np

from autograd import grad
```

deux points à retenir

* le package expose **les mêmes fonctions** que numpy mais **modifiées** pour pouvoir être dérivées

  donc à partir d'ici la variable `np` désigne **le code autograd** et non pas le code numpy; mais il s'utilise exactement pareil
  
* la fonction `grad` retourne la dérivée (en fait le gradient) de son paramètre (une fonction, donc)

+++

## à vous d'essayer

+++

### Q1

+++

calculez le domaine des réels entre 0 et 2π

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

X = np.linspace(0, 2*np.pi)
```

### Q2

+++

appliquez à ce domaine la dérivée de *sin*

**[indice]** on rappelle que pour appliquer une fonction sur un tableau, il faut qu'elle soit vectorisée

```{code-cell} ipython3
# votre code
# votre job est de définir sin_der qui
# est la fonction dérivée de sinus
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

sin_der = grad(np.sin)
```

prune-cell

attention à ce stade on n'a pas une fonction vectorisée

```{code-cell} ipython3
:tags: [level_basic, raises-exception]

sin_der(0.)
```

```{code-cell} ipython3
:tags: [level_basic]

# mais
try:
    sin_der(X)
except Exception as exc:
    print(f"{type(exc)} - {exc}")
```

```{code-cell} ipython3
:tags: [level_basic, raises-exception]

# du coup on vectorise avec numpy
sin_der_vec = np.vectorize(sin_der)
```

### Q3

+++

vérifiez que vous obtenez bien le *cos* de ce domaine

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell

# ça marche toujours ?
sin_der_vec(0.)
```

```{code-cell} ipython3
# prune-cell

Y2 = sin_der_vec(X)
Y = np.cos(X)
Y == Y2
```

```{code-cell} ipython3
# prune-cell

import matplotlib.pyplot as plt
%matplotlib ipympl

fig, (top, bottom) = plt.subplots(nrows=2)
top.plot(X, Y)
top.set_title("cos")
bottom.plot(X, Y2)
bottom.set_title("sin derivée")
;
```

***
