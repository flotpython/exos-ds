---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Taylor (1/3): intro à autograd

+++

le package est ici

* sources <https://github.com/HIPS/autograd>

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
# À LA PLACE de l'habituel 'import numpy as np'
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

# X = ...
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-cell

X = np.linspace(0, 2*np.pi)
```

### Q2

+++

1. utilisez la librairie `grad` pour calculer `sin_der`, une fomction dérivée de la fonction *sin*
2. appliquez-la à ce domaine

**[indice]** on rappelle que pour appliquer une fonction sur un tableau, il faut qu'elle soit vectorisée

```{code-cell} ipython3
# votre code
#
# votre job est de définir sin_der qui
# est la fonction dérivée de sinus
```

```{code-cell} ipython3
# et pour tester
#
sin_der(X)
```

```{code-cell} ipython3
:tags: [level_basic]

# prune-begin

sin_der = grad(np.sin)
```


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

# du coup on vectorise
#
# dans ce contexte on ne peut pas utiliser la syntaxe '@' du décorateur
# et on est obligé d'appliquer le décorateur à la main
#
sin_der = np.vectorize(sin_der)
```

```{code-cell} ipython3
# prune-end
```

### Q3

+++

vérifiez que vous obtenez bien le *cos* de ce domaine

```{code-cell} ipython3
# votre code
```

```{code-cell} ipython3
# prune-cell

# même pas besoin de np.isclose !

Y = np.cos(X)
Y2 = sin_der(X)

np.all(Y == Y2)
```

### Q4 (optionnel)

affichez les courbes des deux fonctions (cosinus et sa dérivée) une au dessus de l'autre

```{code-cell} ipython3
# prune-cell

# c'est mieux avec le mode interactif
%matplotlib ipympl

import matplotlib.pyplot as plt


# on crée les deux sous-figures (que pyplot appelle aussi des axes)
fig, (top, bottom) = plt.subplots(nrows=2)

# on dessine la courbe du haut et son titre
top.plot(X, Y)
top.set_title("cos")
# pareil
bottom.plot(X, Y2)
bottom.set_title("sin derivée")

# c'est optionnel de faire ceci
# plt.show()

# on finit par un point-virgule pour évitez l'affichage du dernier résultat de la cellule
;
```

***
