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

### Q3

+++

vérifiez que vous obtenez bien le *cos* de ce domaine

```{code-cell} ipython3
# votre code
```

### Q4 (optionnel)

affichez les courbes des deux fonctions (cosinus et sa dérivée) une au dessus de l'autre

+++

***
